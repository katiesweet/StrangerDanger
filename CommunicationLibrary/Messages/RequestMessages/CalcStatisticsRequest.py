#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Request import Request


class CalcStatisticsRequest(Request):

    def __init__(self, timePeriod, statsType, data, clientEndpoint):
        super(CalcStatisticsRequest, self).__init__()
        self.timePeriod = timePeriod
        self.statsType = statsType # expecting this to be {'hourly', 'daily'} or {'hourly'} or something.
        self.data = data # expected to be already filtered to the right user (handling filter for time period within stats server)
        # for example: data = [{"timeStamp": "2017-11-29 16:48:30.225099", "camName": "ShemCam", "picLocation": "PhotoDatabase/ShemCam_2017-12-05_18:48:30:225099.jpg"}, {"timeStamp": "2017-12-05 14:52:06.333694", "camName": "ShemCam", "picLocation": "PhotoDatabase/ShemCam_2017-12-05_18:52:06:333694.jpg"}, {"timeStamp": "2017-12-05 02:52:33.340629", "camName": "ShemCam", "picLocation": "PhotoDatabase/ShemCam_2017-12-05_18:52:33:340629.jpg"}]

        self.clientEndpoint = clientEndpoint
