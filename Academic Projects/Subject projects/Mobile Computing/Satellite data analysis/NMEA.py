from math import radians, cos, sin, asin, sqrt
import csv

class nmea:
    def __init__(self,f):
        file=open(f, 'r')
        self.row=[]
        self.new_line='\n'
        for line in file.readlines():
            for i in self.new_line:
                line=line.replace(self.new_line,"")
                self.row.append([line])

    def GPGGA_func(self):
        self.GPGGA=[]
        self.GGA_temp = []
        self.GGA = []
        for i in range(len(self.row)):
            if [w[1:6:] for w in self.row[i]] == ["GPGGA"]:
                self.GPGGA.append(self.row[i])
        for i in range(len(self.GPGGA)):
            self.GGA_temp.append(''.join(self.GPGGA[i]).split(','))
        for i in range(len(self.GGA_temp)):
            if self.GGA_temp[i][1] != "":
                self.GGA.append(self.GGA_temp[i])

    def GPRMC_func(self):
        self.GPRMC = []
        self.RMC_temp = []
        self.RMC = []
        for i in range(len(self.row)):
            if [w[1:6:] for w in self.row[i]] == ["GPRMC"]:
                self.GPRMC.append(self.row[i])
        for i in range(len(self.GPRMC)):
            self.RMC_temp.append(''.join(self.GPRMC[i]).split(','))
        for i in range(len(self.RMC_temp)):
            if self.RMC_temp[i][1] != "":
                self.RMC.append(self.RMC_temp[i])
        self.date = self.RMC[0][9][:2:] + '-' + self.RMC[0][9][2:4:] + '-' + self.RMC[0][9][4:6:]

    def GPGSA_func(self):
        self.GPGSA = []
        self.GSA_temp = []
        self.GSA = []
        for i in range(len(self.row)):
            if [ww[1:6:] for ww in self.row[i]] == ["GPGSA"]:
                self.GPGSA.append(self.row[i])
        for i in range(len(self.GPGSA)):
            self.GSA_temp.append(''.join(self.GPGSA[i]).split(','))
        for i in range(len(self.GSA_temp)):
            if self.GSA_temp[i][16] != "":
                self.GSA.append(self.GSA_temp[i])

    def GPGSV_func(self):
        self.GPGSV = []
        self.GSV_temp = []
        self.GSV = []
        for i in range(len(self.row)):
            if [ww[1:6:] for ww in self.row[i]] == ["GPGSV"]:
                self.GPGSV.append(self.row[i])
        for i in range(len(self.GPGSV)):
            self.GSV_temp.append(''.join(self.GPGSV[i]).split(','))
        for i in range(len(self.GSV_temp)):
            if len(self.GSV_temp[i]) == 20 and self.GSV_temp[i][4] != "" and self.GSV_temp[i][5] != "" and self.GSV_temp[i][6] != "" and \
                    self.GSV_temp[i][7] != "":
                self.GSV.append(self.GSV_temp[i])
        # print(len(self.GSV))
        # print(self.GSV[0])

    def haversine_formula(self,lat1, lon1, lat2, lon2):
        # To calculate the great circle distance between two points on the earth (specified in decimal degrees)
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r_km = 6371  # R of E in kilometers
        r_m=3956  #3956 for miles
        res1=c*r_km
        res2=c*r_m
        return res1,res2

    def write_to_csv_file(self):
        # output_file='E:/Bals/Study plan/Lectures_Tutorials/Sem 3/Mobile Computing/Output.csv'
        lat0 = (float(self.GGA[0][2][:2:]) + (float(self.GGA[0][2][2::]) / 60))
        lon0 = (float(self.GGA[0][4][:3:]) + (float(self.GGA[0][4][3::]) / 60))
        with open(output_file, mode='w') as wr_file:
            doc_writer = csv.writer(wr_file)
            doc_writer.writerow(
                ['Date and Time', 'Latitude', 'Longitude', 'Distance in kilometre(s)','Distance in mile(s)', 'Altitude', 'Fix', 'Sat', 'pdop', 'vdop', 'hdop','height of geoid', 'MagVar','PRN','Elevation','Azimuth','Signal Strength','Speed(m/s)','Course'])
            for i in range(len(self.GGA)):
                if self.GGA[i][1][5:6:] == '0' or self.GGA[i][1][5:6:] == '5':
                    global lat, lon
                    if self.GGA[i][3] == 'N' or 'E':
                        lat = (float(self.GGA[i][2][:2:]) + (float(self.GGA[i][2][2::]) / 60))
                    if self.GGA[i][3] == 'S' or 'W':
                        lat = -(float(self.GGA[i][2][:2:]) + (float(self.GGA[i][2][2::]) / 60))
                    if self.GGA[i][5] == 'E' or 'N':
                        lon = (float(self.GGA[i][4][:3:]) + (float(self.GGA[i][4][3::]) / 60))
                    if self.GGA[i][5] == 'W' or 'S':
                        lon = -(float(self.GGA[i][4][:3:]) + (float(self.GGA[i][4][3::]) / 60))

                    doc_writer.writerow( (( self.date +' '+ self.GGA[i][1][:2:]+":"+self.GGA[i][1][2:4:]+":"+self.GGA[i][1][4:6:]),lat,lon,
self.haversine_formula(lat0,lon0,lat,lon)[0],self.haversine_formula(lat0,lon0,lat,lon)[1],self.GGA[i][9], self.GGA[i][6], self.GGA[i][7], self.GSA[i][15] , self.GSA[i][16], self.GSA[i][17][:3:] , self.GGA[i][11], self.RMC[i][10], self.GSV[i][4],self.GSV[i][5], self.GSV[i][6], self.GSV[i][7], float(self.RMC[i][7])*(0.514444), self.RMC[i][8] ))
            print("\nDetails Exported in csv file:",'"'+output_file+'"')


    def write_to_xml_file(self):
        Time="20"+self.RMC[0][9][4:6:]+'-'+self.RMC[0][9][2:4:]+'-'+self.RMC[0][9][:2:]+"T"
        # filepath="E:/Bals/Study plan/Lectures_Tutorials/Sem 3/Mobile Computing/Output.xml"
        global file1
        file1 = open(filepath, 'w+')
        start='''<?xml version='1.0' encoding='ISO-8859-1' ?>
<gpx version="1.1" creator="TrekBuddy 0.9.99" xmlns="http://www.topografix.com/GPX/1/1" xmlns:nmea="http://trekbuddy.net/2009/01/gpx/nmea" xmlns:gsm="http://trekbuddy.net/2009/01/gpx/gsm">
 <trk>
  <trkseg>'''
        print(start,file=file1)
        for i in range(len(self.GGA)):
            if self.GGA[i][1][5:6:] == '0' or self.GGA[i][1][5:6:] == '5':
                global lat, lon
                if self.GGA[i][3] == 'N' or 'E':
                    lat = (float(self.GGA[i][2][:2:]) + (float(self.GGA[i][2][2::]) / 60))
                if self.GGA[i][3] == 'S' or 'W':
                    lat = -(float(self.GGA[i][2][:2:]) + (float(self.GGA[i][2][2::]) / 60))
                if self.GGA[i][5] == 'E' or 'N':
                    lon = (float(self.GGA[i][4][:3:]) + (float(self.GGA[i][4][3::]) / 60))
                if self.GGA[i][5] == 'W' or 'S':
                    lon = -(float(self.GGA[i][4][:3:]) + (float(self.GGA[i][4][3::]) / 60))

                Date = self.GGA[i][1][:2:] + ":" + self.GGA[i][1][2:4:] + ":" + self.GGA[i][1][4:6:] + ".Z"
                print('   <trkpt lat="' + str(lat) + '" lon="' + str(lon) + '">', file=file1)
                print('\t<ele>' + self.GSV[i][5] + '</ele>', file=file1)
                print('\t<time>' + Time + Date + '</time>', file=file1)
                print('\t<fix>' + str(self.GGA[i][6]) + '</fix>', file=file1)
                print('\t <sat>' + str(self.GGA[i][7]) + '</sat>', file=file1)
                print('\t <extensions>', file=file1)
                print('\t <gsv:satellites>', file=file1)
                # for i in range(len(self.GGA)):
                print('\t  <gsv:' + str(self.GSV[i][3]) + ' prn="' + str(self.GSV[i][4]) + '" elevation="' + str(
                    self.GSV[i][5]) + '" ' + 'azimuth="' + str(self.GSV[i][6]) + ' " ' + 'sat="' + str(
                    self.GSV[i][7]) + '"', file=file1)
                print('\t </gsv:satellites>', file=file1)
                print('\t<nmea:course>' + str(self.RMC[i][8]) + '</nmea:course>', file=file1)
                print('\t<nmea:speed>' + str(float(self.RMC[i][7]) * (0.514444)) + '</nmea:speed>', file=file1)
                print('\t </extensions>', file=file1)
                print('\t</trkpt>', file=file1)
                end = '''  </trkseg>
                 </trk>
                </gpx>'''
                print(end,file=file1)
        print("Details Exported in xml file:", '"' +filepath+'"')


# t=nmea("C:/Users/Bala/Desktop/2017-11-02.nmea.txt")
t.GPGGA_func()
t.GPRMC_func()
t.GPGSA_func()
t.GPGSV_func()
t.write_to_csv_file()
t.write_to_xml_file()