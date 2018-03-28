import taxi
import csv
import time

start_time = time.time()

fd = open("m_under1100m.csv","w")
ft = open("s_under100s.csv","w")

check_fd = 0
check_ft = 0

count_fd = 0
count_ft = 0
count_al = 0

with open("d4_fig.csv","r") as f:
    r = csv.reader(f,delimiter=',')
    for p in r :
        d = float(p[0])
        t = float(p[1])
        if d < 1100 :
            fd.write('{}, {}\n'.format(d,t))
            count_fd += 1
            check_fd = 1

        if t < 100 :
            ft.write('{}, {}\n'.format(d,t))
            count_ft += 1
            check_ft = 1

        if check_fd == 1 and check_ft == 1 :
            count_al += 1

        check_ft = 0
        check_fd = 0

print("count_fd")
print(count_fd)
print("count_ft")
print(count_ft)
print("count_al")
print(count_al)
