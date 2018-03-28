import numpy
import csv
import taxi
import sys

folder_name = ['2013-12-11/','2013-12-12/','2013-12-13/','2013-12-14/','2013-12-15/','2017-05-15/','2017-05-16/','2017-05-17/','2017-05-18/','2017-05-19/','2017-05-20/','2017-05-21/']
#folder_name = ['2017-05-15/']
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

D = {}
fp = open("d-overhangd.dat","w")

for folder in folder_name :
    for DAT in DAT_name :
        filename = "source/"+folder+DAT
        print(filename)
        with open(filename,'r') as f:
            r = csv.reader(f,delimiter=',')
            try:
                for p in r :
                    if taxi.chk_in_kor(p[1],p[2]) :
                        if int(p[8]) :
                            taxi_id = int(p[0])
                            if taxi_id in D:
                                D[taxi_id].append((p[1],p[2]))
                            else :
                                D[taxi_id]=[(p[1],p[2])]
                        else :
                            if taxi_id in D:
                                t_list = D[taxi_id]
                                l = len(t_list)
                                if l > 2 :
                                    s_lon = t_list[0][0]
                                    s_lat = t_list[0][1]
                                    d_lon = t_list[l-1][0]
                                    d_lat = t_list[l-1][1]
                                    temp_d = 0
                                    totl_d = 0
                                    dest_d = taxi.gps_to_d(s_lon,s_lat,d_lon,d_lat)
                                    ovrh_d = 0
                                    svrh_d = 0
                                    for i in range(0,l-1) :
                                        temp_d = taxi.gps_to_d(t_list[i][0],t_list[i][1],t_list[i+1][0],t_list[i+1][1])
                                        totl_d += temp_d
                                        if taxi.gps_to_d(t_list[i][0],t_list[i][1],d_lon,d_lat) < taxi.gps_to_d(t_list[i+1][0],t_list[i+1][1],d_lon,d_lat) :
                                            svrh_d += temp_d
                                        if taxi.gps_to_d(s_lon,s_lat,t_list[i][0],t_list[i][1]) > dest_d or taxi.gps_to_d(s_lon,s_lat,t_list[i+1][0],t_list[i+1][1]) > dest_d :
                                            ovrh_d += temp_d
                                    if ovrh_d > 0 :
                                        fp.write('{}, {}, {}, {}, {}\n'.format(totl_d,ovrh_d,svrh_d,dest_d,p[4]))
                                D[taxi_id] = []
                            else :
                                D[taxi_id] = []
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(filename, r.line_num, e))

fp.close()
