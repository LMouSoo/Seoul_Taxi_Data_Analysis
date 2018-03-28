import csv
import sys
from math import radians,sin,cos,atan2,sqrt


def distance(lon1,lat1,lon2,lat2):
    R = 6371000
    p1 = radians(float(lat1)*0.0000001)
    p2 = radians(float(lat2)*0.0000001)
    dp = radians(float(lat2)*0.0000001-float(lat1)*0.0000001)
    dl = radians(float(lon2)*0.0000001-float(lon1)*0.0000001)

    a = (sin(dp/2)*sin(dp/2)) + (cos(p1)*cos(p2)*sin(dl/2)*sin(dl/2))

    c = 2*atan2(sqrt(a),sqrt(1-a))

    d = R*c

    return d

def tance(lon,lat,dst,dgr):
    R = 6371000
    x_dst = dst*cos(dgr)
    y_dst = dst*sin(dgr)

    cos(x_dst/R)=sin(lat)*sin(lat_x)+cos(lat




print('''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>seoul traffic analysis</name>
    <description>blablaseoul blablatraffic blablaanalysis</description>
    <Style id="icon-1899-0288D1-normal">
      <IconStyle>
        <color>ffd18802</color>
        <scale>1</scale>
        <Icon>
          <href>http://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
        <hotSpot x="16" xunits="pixels" y="32" yunits="insetPixels"/>
      </IconStyle>
      <LabelStyle>
        <scale>0</scale>
      </LabelStyle>
    </Style>
    <Style id="icon-1899-0288D1-highlight">
      <IconStyle>
        <color>ffd18802</color>
        <scale>1</scale>
        <Icon>
          <href>http://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
        <hotSpot x="16" xunits="pixels" y="32" yunits="insetPixels"/>
      </IconStyle>
      <LabelStyle>
        <scale>1</scale>
      </LabelStyle>
    </Style>
    <StyleMap id="icon-1899-0288D1">
      <Pair>
        <key>normal</key>
        <styleUrl>#icon-1899-0288D1-normal</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#icon-1899-0288D1-highlight</styleUrl>
      </Pair>
    </StyleMap>
    <Style id="poly-000000-1200-77-normal">
      <LineStyle>
        <color>ff000000</color>
        <width>1.2</width>
      </LineStyle>
      <PolyStyle>
        <color>4d000000</color>
        <fill>1</fill>
        <outline>1</outline>
      </PolyStyle>
    </Style>
    <Style id="poly-000000-1200-77-highlight">
      <LineStyle>
        <color>ff000000</color>
        <width>1.8</width>
      </LineStyle>
      <PolyStyle>
        <color>4d000000</color>
        <fill>1</fill>
        <outline>1</outline>
      </PolyStyle>
    </Style>
    <StyleMap id="poly-000000-1200-77">
      <Pair>
        <key>normal</key>
        <styleUrl>#poly-000000-1200-77-normal</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#poly-000000-1200-77-highlight</styleUrl>
      </Pair>
    </StyleMap>''')

#folder_name = ['2013-12-11/','2013-12-12/','2013-12-13/','2013-12-14/','2013-12-15/','2017-05-15/','2017-05-16/','2017-05-17/','2017-05-18/','2017-05-19/','2017-05-20/','2017-05-21/']
folder_name = ['2017-05-15/','2017-05-16/','2017-05-17/']
DAT_name = []
for i in range(0,24):
    for n in range(0,6):
        for t in [0,2,5,7]:
            if t == 0 or t == 5:
                ss = 0
            else:
                ss = 3
            if i < 10 :
                DAT_name.append("0{}{}{}{}0.DAT".format(i,n,t,ss))
            else:
                DAT_name.append("{}{}{}{}0.DAT".format(i,n,t,ss))


for folder in folder_name :
    print('''    <Folder>
      <name>{}</name>'''.format(folder))
    for DAT in DAT_name :
        filename = "source/"+folder+DAT

        total_event = 0
        total_sum_x = 0
        total_sum_y = 0
        

        with open(filename,'r') as f:
            r = csv.reader(f, delimiter=',')
            try:
                for p in r :
                    if float(p[1]) < 1295847220 and float(p[1]) > 1261116670 and float(p[2]) > 342922220 and float(p[2]) < 386111110 :
                        total_event += 1
                        total_sum_x += float(p[1])
                        total_sum_y += float(p[2])
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(filename, r.line_num, e))


        mean_x = total_sum_x/total_event
        mean_y = total_sum_y/total_event

        #print('x:{}, y:{}'.format(mean_x, mean_y))

        exp_mean = 0
        mean_exp = 0

        R_list=[]

        with open(filename,'r') as f:
            r = csv.reader(f, delimiter=',')
            try:
                for p in r:
                    if float(p[1]) < 1295847220 and float(p[1]) > 1261116670 and float(p[2]) > 342922220 and float(p[2]) < 386111110 :
                        temp_r = distance(p[1],p[2],mean_x,mean_y)
                        R_list.append(temp_r)
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(filename, r.line_num, e))


        R_list.sort()

        RR = []
        RR.append(R_list[int(total_event * 0.682689492137)])
        RR.append(R_list[int(total_event * 0.954499736104)])
        RR.append(R_list[int(total_event * 0.997300203937)])

        print('''      <Placemark>
        <name>{} point</name>
        <description>{},{}</description>
        <styleUrl>#icon-1899-0288D1</styleUrl>
        <Point>
          <coordinates>
            {},{},0
          </coordinates>
        </Point>
      </Placemark>'''.format(DAT,int(mean_x)*0.0000001,int(mean_y)*0.0000001,int(mean_x)*0.0000001,int(mean_y)*0.0000001))
        for PR in RR :
            print('''      <Placemark>
        <name>{} Polygon</name>
        <description>{},{}</description>
        <styleUrl>#poly-000000-1200-77</styleUrl>
        <Polygon>
          <outerBoundaryIs>
            <LinearRing>
              <tessellate>1</tessellate>
              <coordinates>
                {},{},0
                {},{},0
                {},{},0
                {},{},0
                {},{},0
              </coordinates>
            </LinearRing>
          </outerBoundaryIs>
        </Polygon>
      </Placemark>'''.format(DAT, int(mean_x)*0.0000001, int(mean_y)*0.0000001 ,int(mean_x-PR)*0.0000001,int(mean_y)*0.0000001, int(mean_x)*0.0000001,int(mean_y+PR)*0.0000001, int(mean_x+PR)*0.0000001,int(mean_y)*0.0000001, int(mean_x)*0.0000001,int(mean_y-PR)*0.0000001, int(mean_x-PR)*0.0000001,int(mean_y)*0.0000001))

    print('''    </Folder>''')

print('''  </Document>
</kml>''')


        #print('''total event : {}, 68.26% Radius : {}, 95.44% Radius : {}, 99.73% Radius : {}'''.format(total_event,R68,R95,R99))
