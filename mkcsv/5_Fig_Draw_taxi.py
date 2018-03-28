import numpy
import csv
import taxi
import sys
import time

start_time = time.time()

#folder_name = ['2013-12-11/','2013-12-12/','2013-12-13/','2013-12-14/','2013-12-15/','2017-05-15/','2017-05-16/','2017-05-17/','2017-05-18/','2017-05-19/','2017-05-20/','2017-05-21/']
folder_name = ['2017-05-15/','2017-05-16/','2017-05-17/','2017-05-18/','2017-05-19/','2017-05-20/','2017-05-21/']
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
fp = open("d5_fig_d_10.csv","w")
chk = 0
chk_d = 100000
for folder in folder_name :
    for DAT in DAT_name :
        filename = "/home/lms/traffic/source/"+folder+DAT
        print(filename)
        with open(filename,'r') as f:
            r = csv.reader(f,delimiter=',')
            try:
                for p in r :
                    x = p[1]
                    y = p[2]
                    if taxi.chk_in_kor(x,y) :
                        if int(p[8]) :
                            taxi_id = int(p[0])
                            if taxi_id in D:
                                D[taxi_id].append((int(x),int(y),int(p[4])))
                            else :
                                D[taxi_id]=[(int(x),int(y),int(p[4]))]
                        else :
                            if taxi_id in D:
                                t_list = D[taxi_id]
                                l = len(t_list)
                                if l > 2 :
                                    s_lon = t_list[0][0]
                                    s_lat = t_list[0][1]
                                    pre_d0 = s_lon
                                    pre_d1 = s_lat
                                    pre_t = taxi.int_to_datetime(t_list[0][2])
                                    temp_d = 0
                                    totl_d = 0
                                    d_to_d = 0
                                    prnt_d = 0
                                    for i in range(1,l) :
                                        temp_d0 = t_list[i][0]
                                        temp_d1 = t_list[i][1]
                                        totl_d += taxi.gps_to_d(pre_d0,pre_d1,temp_d0,temp_d1)
                                        d_to_d = taxi.gps_to_d(temp_d0,temp_d1,s_lon,s_lat)
                                        pre_d0 = temp_d0
                                        pre_d1 = temp_d1
                                        if d_to_d > chk_d :
                                            prnt_d = totl_d / d_to_d * chk_d
                                            temp_t = taxi.int_to_datetime(t_list[i][2])
                                            prnt_t = temp_t-pre_t
                                            prnt_t = prnt_t.total_seconds() * chk_d / d_to_d
                                            fp.write('{}, {}\n'.format(prnt_d, prnt_t))
                                            chk += 1
                                            s_lon = temp_d0
                                            s_lat = temp_d1
                                            totl_d = 0
                                            pre_t = temp_t

                                D[taxi_id] = []
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(filename, r.line_num, e))

print(chk)
fp.close()

end_time = time.time() - start_time

print(end_time)


