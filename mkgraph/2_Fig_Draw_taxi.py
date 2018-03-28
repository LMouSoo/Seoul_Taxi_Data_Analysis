import numpy
import csv
import sys
import taxi
from taxi import gps_to_d,d_to_gps,exp_kml_foot,exp_kml_poly,exp_kml_point,exp_kml_head
from math import radians,sin,cos,atan2,sqrt,acos,asin,degrees


folder_name = ['2013-12-11/','2013-12-12/','2013-12-13/','2013-12-14/','2013-12-15/','2017-05-15/','2017-05-16/','2017-05-17/','2017-05-18/','2017-05-19/','2017-05-20/','2017-05-21/']
#folder_name = ['2017-05-15/','2017-05-16/','2017-05-17/']
#folder_name = ['2017-05-16/']
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
    total_event = 0
    total_sum_x = 0
    total_sum_y = 0
    hour_event = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    hour_sum_x = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    hour_sum_y = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for DAT in DAT_name :
        filename = "source/"+folder+DAT
        print("mean "+filename)
        with open(filename,'r') as f:
            r = csv.reader(f, delimiter=',')
            try:
                for p in r :
                    if float(p[1]) < 1295847220 and float(p[1]) > 1261116670 and float(p[2]) > 342922220 and float(p[2]) < 386111110 :
                        total_event += 1
                        total_sum_x += float(p[1])
                        total_sum_y += float(p[2])
                        hour_event[int(p[4][8:10])] += 1
                        hour_sum_x[int(p[4][8:10])] += float(p[1])
                        hour_sum_y[int(p[4][8:10])] += float(p[2])
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(filename, r.line_num, e))

    mean_x = total_sum_x/total_event
    mean_y = total_sum_y/total_event
    hour_mean_x = []
    hour_mean_y = []
    for i in range(0,24):
        if hour_event[i] != 0 :
            hour_mean_x.append(hour_sum_x[i]/hour_event[i])
            hour_mean_y.append(hour_sum_y[i]/hour_event[i])
        else:
            hour_mean_x.append(0)
            hour_mean_y.append(0)

    R_list=[]
    hour_R_list=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

    for DAT in DAT_name :
        filename = "source/"+folder+DAT
        print("D "+filename)
        with open(filename,'r') as f:
            r = csv.reader(f, delimiter=',')
            try:
                for p in r:
                    if float(p[1]) < 1295847220 and float(p[1]) > 1261116670 and float(p[2]) > 342922220 and float(p[2]) < 386111110 :
                        temp_r = gps_to_d(p[1],p[2],mean_x,mean_y)
                        R_list.append(temp_r)
                        if hour_event[int(p[4][8:10])] != 0 :
                            temp_hr = gps_to_d(p[1],p[2],hour_mean_x[int(p[4][8:10])],hour_mean_y[int(p[4][8:10])])
                            hour_R_list[int(p[4][8:10])].append(temp_hr)
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(filename, r.line_num, e))


    R_list.sort()

    RR68 = R_list[int(total_event * 0.682689492137)]
    RR95 = R_list[int(total_event * 0.954499736104)]
    RR99 = R_list[int(total_event * 0.997300203937)]

    exp_kml_head(folder[:-1],folder[:-1])

    for i in range(0,24):
        if hour_event[i] != 0:
            hour_R_list[i].sort()
            RH68 = hour_R_list[i][int(hour_event[i] * 0.682689492137)]
            RH95 = hour_R_list[i][int(hour_event[i] * 0.954499736104)]
            RH99 = hour_R_list[i][int(hour_event[i] * 0.997300203937)]

            exp_kml_point(hour_mean_x[i],hour_mean_y[i],folder[:-1],i)
            exp_kml_poly(hour_mean_x[i],hour_mean_y[i],RH68,folder[:-1],"{}_68".format(i),RH68)
            exp_kml_poly(hour_mean_x[i],hour_mean_y[i],RH95,folder[:-1],"{}_95".format(i),RH95)
            exp_kml_poly(hour_mean_x[i],hour_mean_y[i],RH99,folder[:-1],"{}_99".format(i),RH99)

    #print('''total event : {}, 68.26% Radius : {}, 95.44% Radius : {}, 99.73% Radius : {}'''.format(total_event,RR[0],RR[1],RR[2]))
    #print('''{}, {}, {}, {}, {}, {}, {}, {}'''.format(folder, DAT, total_event, mean_x, mean_y, RR[0], RR[1], RR[2]))
    exp_kml_point(mean_x,mean_y,folder[:-1],"total")
    exp_kml_poly(mean_x,mean_y,RR68,folder[:-1],"total_68",RR68)
    exp_kml_poly(mean_x,mean_y,RR95,folder[:-1],"total_95",RR95)
    exp_kml_poly(mean_x,mean_y,RR99,folder[:-1],"total_99",RR99)

    exp_kml_foot(folder[:-1])


"""
for folder in folder_name :
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


        exp_mean = 0
        mean_exp = 0

        R_list=[]

        with open(filename,'r') as f:
            r = csv.reader(f, delimiter=',')
            try:
                for p in r:
                    if float(p[1]) < 1295847220 and float(p[1]) > 1261116670 and float(p[2]) > 342922220 and float(p[2]) < 386111110 :
                        temp_r = gps_to_d(p[1],p[2],mean_x,mean_y)
                        R_list.append(temp_r)
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(filename, r.line_num, e))


        R_list.sort()

        RR = []
        RR.append(R_list[int(total_event * 0.682689492137)])
        RR.append(R_list[int(total_event * 0.954499736104)])
        RR.append(R_list[int(total_event * 0.997300203937)])
        #print('''total event : {}, 68.26% Radius : {}, 95.44% Radius : {}, 99.73% Radius : {}'''.format(total_event,RR[0],RR[1],RR[2]))
        print('''{}, {}, {}, {}, {}, {}, {}, {}'''.format(folder, DAT, total_event, mean_x, mean_y, RR[0], RR[1], RR[2]))
"""
