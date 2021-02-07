class Location:
    def __init__(self, globalID, date, status, xloc, yloc):
        self.xloc = float(xloc)
        self.yloc = float(yloc)
        self.globalID = globalID
        self.status = status
        self.date = date

    def get_loc(self):
        return self.xloc, self.yloc

    def get_id(self):
        return self.globalID

    def get_status(self):
        return self.status

    def get_date(self):
        return self.date

    def to_string(self):
        return self.globalID + " " + self.date + " " \
               + self.status + " " + str(self.xloc) + " " + str(self.yloc)
