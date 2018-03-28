import numpy
import csv
import sys
from math import radians,sin,cos,atan2,sqrt,acos,asin,degrees

"""
Lead author : Kim Hyun-Soo (soo9211@gmail.com, University of Seoul)

#Some calculations on the basis of a spherical earth(ignoring ellipsoidal effects).
#The earth is very slighty ellipsoidal, using a spherical model gives errors typically up to 0.3%
#You want more information about spherical model error, please see this link = https://gis.stackexchange.com/questions/25494/how-accurate-is-approximating-the-earth-as-a-sphere#25580
#if You want a calculation that uses the ellipsoidal effects, please see this link = http://www.movable-type.co.uk/scripts/latlong-vincenty.html (Vincenty solutions of geodesics on the ellipsoid)


#Reference

#Calculate distance, bearing and more between Latitude/Longitude points (http://www.movable-type.co.uk/scripts/latlong.html)

"""

def gps_to_d(lon1,lat1,lon2,lat2,formula='haversine'):
    R = 6371000
    p1 = radians(float(lat1)*0.0000001)
    p2 = radians(float(lat2)*0.0000001)
    dp = radians(float(lat2)*0.0000001-float(lat1)*0.0000001)
    dl = radians(float(lon2)*0.0000001-float(lon1)*0.0000001)

    if formula == 'haversine' : # haversine formula - basic
        a = sin(dp/2)**2 + cos(p1)*cos(p2)*(sin(dl/2)**2)
        c = 2*atan2(sqrt(a),sqrt(1-a))
        d = R*c

    if formula == 'SLC' : # Spherical Law of Cosines - Simple.. but maybe slightly slower than the haversine //  error ~ 0.0000001
        d = acos(sin(p1)*sin(p2) + cos(p1)*cos(p2)*cos(dl))*R

    if formula == 'EA' : # Equirectangular approximation - performance is good / accuracy is very bad // error ~ 0.1
        x = dl*cos((p1+p2)/2)
        y = dp
        d = sqrt(x**2 + y**2)*R

    return d



def d_to_gps(lon,lat,brng,d):
    lon = radians(float(lon)*0.0000001)
    lat = radians(float(lat)*0.0000001)
    brng = radians(brng)
    R = 6371000

    r_lat = asin(sin(lat)*cos(d/R) + cos(lat)*sin(d/R)*cos(brng))
    r_lon = lon + atan2(sin(brng)*sin(d/R)*cos(lat), cos(d/R)-sin(lat)*sin(r_lat))

    r_lat = degrees(r_lat)
    r_lon = degrees(r_lon)

    return int(r_lon*10000000),int(r_lat*10000000)



def chk_in_kor(lon,lat):
    if int(lon) < 1295847220 and int(lon) > 1261116670 and int(lat) > 342922220 and int(lat) < 386111110 :
        return 1
    else :
        return 0


def exp_kml_head(file_name='defult',layer_name='defult'):
    print("output4/{}.kml_head".format(file_name))
    fp = open("output4/{}.kml".format(file_name),"a")
    fp.write('''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>{}</name>
    <Style id="icon-1502-0288D1-normal">
      <IconStyle>
        <color>ffd18802</color>
        <scale>1</scale>
        <Icon>
          <href>http://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
      </IconStyle>
      <LabelStyle>
        <scale>0</scale>
      </LabelStyle>
    </Style>
    <Style id="icon-1502-0288D1-highlight">
      <IconStyle>
        <color>ffd18802</color>
        <scale>1</scale>
        <Icon>
          <href>http://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
      </IconStyle>
      <LabelStyle>
        <scale>1</scale>
      </LabelStyle>
    </Style>
    <StyleMap id="icon-1502-0288D1">
      <Pair>
        <key>normal</key>
        <styleUrl>#icon-1502-0288D1-normal</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#icon-1502-0288D1-highlight</styleUrl>
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
    </StyleMap>
'''.format(layer_name))
    fp.close()

def exp_kml_point(lon,lat,file_name='defult',point_name='defult',point_script='empty'):
    print("output4/{}.kml_point_{}".format(file_name,point_name))
    fp = open("output4/{}.kml".format(file_name),"a")
    fp.write('''    <Placemark>
      <name>{}</name>
      <description>{}</description>
      <styleUrl>#icon-1502-0288D1</styleUrl>
      <Point>
        <coordinates>
          {},{},0
        </coordinates>
      </Point>
    </Placemark>
'''.format(point_name,point_script,lon*0.0000001,lat*0.0000001))
    fp.close()

def exp_kml_poly(lon,lat,d,file_name='defult',poly_name='defult',poly_script='empty'):
    print("output4/{}.kml_head".format(file_name))
    fp = open("output4/{}.kml".format(file_name),"a")
    fp.write('''    <Placemark>
      <name>{}</name>
      <description>{}</description>
      <styleUrl>#poly-000000-1200-77</styleUrl>
      <Polygon>
        <outerBoundaryIs>
          <LinearRing>
            <tessellate>1</tessellate>
            <coordinates>'''.format(poly_name,poly_script))
    for i in range(0,360):
        temp=d_to_gps(lon,lat,i,d)
        fp.write('''              {},{},0'''.format(temp[0]*0.0000001,temp[1]*0.0000001))

    fp.write('''            </coordinates>
          </LinearRing>
        </outerBoundaryIs>
      </Polygon>
    </Placemark>
''')
    fp.close()

def exp_kml_foot(file_name='defult'):
    print("output4/{}.kml_foot".format(file_name))
    fp = open("output4/{}.kml".format(file_name),"a")
    fp.write('''  </Document>
</kml>''')
    fp.close()


