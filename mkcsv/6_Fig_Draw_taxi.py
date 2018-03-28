import numpy
import csv
import taxi
import sys
import time

start_time = time.time()

#folder_name = ['2013-12-11/','2013-12-12/','2013-12-13/','2013-12-14/','2013-12-15/','2017-05-15/','2017-05-16/','2017-05-17/','2017-05-18/','2017-05-19/','2017-05-20/','2017-05-21/']
#folder_name = ['2017-05-15/','2017-05-16/','2017-05-17/','2017-05-18/','2017-05-19/','2017-05-20/','2017-05-21/']
folder_name = ['2017-05-15/']

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

cell = {}
fp = open("d6_fig_2017-05-15.csv","w")
chk = 0
center = (1269779410,375663060)

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
                        cell_id = taxi.gps_to_cell(center,(x,y))
                        if cell_id in cell:
                            cell[cell_id] += 1
                        else :
                            cell[cell_id] = 1

                fp.write('{}'.format(cell))

            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(filename, r.line_num, e))

#print(chk)
fp.close()

end_time = time.time() - start_time

print(end_time)


