#!/usr/bin/python

#############################################
#
# Credit for the motion detection algorithm
# and opencv utils to Adrian Rosebrock
# at www.pyimagesearch.com
#
#############################################
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import warnings
import json
import imutils
import cv2
import datetime
import time
import thread
import sys
sys.path.append('../')

import logging
logging.basicConfig(filename="Camera.log", level=logging.DEBUG, \
    format='%(asctime)s - %(levelname)s - %(module)s - Thread: %(thread)d -\
    %(message)s')

from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem
from CommunicationLibrary.Messages.RequestMessages import *
from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.SharedObjects import *

class Camera():
    def __init__(self):
        logging.info("Creating camera process")
        self.shouldRun = True
        self.comm = CommunicationSubsystem.CommunicationSubsystem()
        self.registrationServerAddress = ("192.168.0.5", 50000)
        #self.registrationServerAddress = ("34.209.72.192", 50000)
        self.mainServerAddress = (None, None)
        self.canStartSending = False

        self.sendRegisterRequest()
        thread.start_new_thread(self.checkForMessagesPeriodically,())
        thread.start_new_thread(self.runVideoStream,())
        while self.shouldRun:
            pass

    def sendRegisterRequest(self):
        message = Envelope(self.registrationServerAddress, RegisterRequest(ProcessType.CameraProcess))
        self.comm.sendMessage(message)
        logging.debug("Sending Register Request message " + repr(message))

    def sendSaveMotionRequest(self, endpoint, frame):
        message = Envelope(endpoint, SaveMotionRequest(frame))
        self.comm.sendMessage(message)
        logging.debug("Sending Save Motion Request message " + repr(message))

    def setupCameraStream(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-c", "--conf", required=True, help="path to the JSON configuration file")
        args = vars(ap.parse_args())
        self.conf = json.load(open(args["conf"]))
        
        # initialize the camera and grab a reference to the raw camera capture
        camera = PiCamera()
        camera.resolution = tuple(self.conf["resolution"])
        camera.framerate = self.conf["fps"]
        return camera

    def scaleAndBlurFrame(self, frame):
        frame = imutils.resize(frame, width=320)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        return gray

    def calcFrameDelta(self, gray, avg):
        # accumulate the weighted average between the current frame and
        # previous frames, then compute the difference between the current
        # frame and running average
        cv2.accumulateWeighted(gray, avg, 0.5)
        return cv2.absdiff(gray, cv2.convertScaleAbs(avg))

    def findContoursAroundMotion(self, frameDelta):
        # threshold the delta image, dilate the thresholded image to fill
        # in holes, then find contours on thresholded image
        thresh = cv2.threshold(frameDelta, self.conf["delta_thresh"], 255,
                cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        return cnts

    def checkContours(self, frame, contours):
        # loop over the contours
        for c in contours:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < self.conf["min_area"]:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.text = "Occupied"
        return frame

    
    def locateMotion(self, frame, gray, avg):
        frameDelta = self.calcFrameDelta(gray, avg)
        contours = self.findContoursAroundMotion(frameDelta)
        return self.checkContours(frame, contours)

    def updateStatusAndTime(self, frame, timestamp):
        # draw the text and timestamp on the frame
        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(frame, "Room Status: {}".format(self.text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (0, 0, 255), 1)
        return frame

    def handleIntruderDetected(self, frame):
        print 'saving image'
        cv2.imwrite('img.jpg', frame)


    def checkForIntruders(self, frame, timestamp):
        # check to see if the room is occupied
        if self.text == "Occupied":
            # check to see if enough time has passed between uploads
            if (timestamp - self.lastUploaded).seconds >= self.conf["min_upload_seconds"]:
                # increment the motion counter
                self.motionCounter += 1

                # check to see if the number of frames with consistent motion is
                # high enough
                if self.motionCounter >= self.conf["min_motion_frames"]:
                    thread.start_new_thread(self.handleIntruderDetected,(frame,))
                    # update the last uploaded timestamp and reset the motion
                    # counter
                    self.lastUploaded = timestamp
                    self.motionCounter = 0

        # otherwise, the room is not occupied
        else:
            self.motionCounter = 0 

    def updateFrame(self, frame, timestamp):
        frame = self.updateStatusAndTime(frame, timestamp)
        self.checkForIntruders(frame, timestamp)


    def captureFrames(self, camera):
        # allow the camera to warmup, then initialize the average frame, last
        # uploaded timestamp, and frame motion counter
        rawCapture = PiRGBArray(camera, size=tuple(self.conf["resolution"]))
        logging.info("Camera is warming up...")
        time.sleep(self.conf["camera_warmup_time"])
        self.lastUploaded = datetime.datetime.now()
        self.motionCounter = 0
        avg = None

        # capture frames from the camera
        for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image and initialize
            # the timestamp and occupied/unoccupied text
            frame = f.array
            timestamp = datetime.datetime.now()
            self.text = "Unoccupied"

            # resize the frame, convert it to grayscale, and blur it
            gray = self.scaleAndBlurFrame(frame)

            # if the average frame is None, initialize it
            if avg is None:
                logging.info("Starting background model...")
                avg = gray.copy().astype("float")
                rawCapture.truncate(0)
                continue

            self.locateMotion(frame, gray, avg)
            self.updateFrame(frame, timestamp)

            # check to see if the frames should be displayed to screen
            if self.conf["show_video"]:
                # display the security feed
                cv2.imshow("Security Feed", frame)
                key = cv2.waitKey(1) & 0xFF
 
                # if the `q` key is pressed, break from the lop
                if key == ord("q"):
                    self.shouldRun = False
                    break
 
            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)

    def runVideoStream(self):
        camera = self.setupCameraStream()
        self.captureFrames(camera)


    def checkForMessagesPeriodically(self):
        while self.shouldRun:
            try:
                haveMessage, envelope = self.comm.getMessage()
                if haveMessage:
                    logging.info('Handling new message')
                    self.processNewMessage(envelope)
            except:
                pass

    def processNewMessage(self, envelope):
        if isinstance(envelope.message, RegisterReply):
            logging.info('Handling Register Reply')
            self.handleRegisterReply(envelope)

    def handleRegisterReply(self, envelope):
        processId = envelope.message.processId

        LocalProcessInfo.setProcessId(processId)
        logging.info('Received ProcessID: {}'.format(LocalProcessInfo.getProcessId()))
        self.canStartSending = True
            

if __name__ == '__main__':
    Camera()
