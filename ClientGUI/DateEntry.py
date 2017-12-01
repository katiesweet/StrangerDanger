from Tkinter import *
from datetime import datetime

class DateEntry(Frame):
    def __init__(self, master, label):
        Frame.__init__(self, master)
        font = ("Calibri", 10)

        nameLabel = Label(self, text=label, font=font)

        self.monthVar = StringVar(self, value="MM")
        self.dayVar = StringVar(self, value="DD")
        self.yearVar = StringVar(self, value="YY")
        self.hourVar = StringVar(self, value="hh")
        self.minVar = StringVar(self, value="mm")
        self.secVar = StringVar(self, value="ss")

        month = Entry(self, width=2, textvariable=self.monthVar, font=font)
        day = Entry(self, width=2, textvariable=self.dayVar, font=font)
        year = Entry(self, width=2, textvariable=self.yearVar, font=font)
        hour = Entry(self, width=2, textvariable=self.hourVar, font=font)
        minute = Entry(self, width=2, textvariable=self.minVar, font=font)
        sec = Entry(self, width=2, textvariable=self.secVar, font=font)

        label1 = Label(self, text='/')
        label2 = Label(self, text='/')
        label3 = Label(self, text=' ')
        label4 = Label(self, text=':')
        label5 = Label(self, text=':')

        nameLabel.pack(side=LEFT)
        month.pack(side=LEFT)
        label1.pack(side=LEFT)
        day.pack(side=LEFT)
        label2.pack(side=LEFT)
        year.pack(side=LEFT)
        label3.pack(side=LEFT)
        hour.pack(side=LEFT)
        label4.pack(side=LEFT)
        minute.pack(side=LEFT)
        label5.pack(side=LEFT)
        sec.pack(side=LEFT)

    def getDate(self):
        month = self.monthVar.get()
        day = self.dayVar.get()
        year = self.yearVar.get()
        hour = self.hourVar.get()
        minute = self.minVar.get()
        sec = self.secVar.get()
        stringTime = month + day + year + hour + minute + sec
        try:
            datetime_object = datetime.strptime(stringTime, '%m%d%y%H%M%S')
            return True, str(datetime_object)
        except:
            return False, str("")
