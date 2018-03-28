import ROOT
import csv

output = ROOT.TFile("center_2013.root","UPDATE")



for day in (11,12,13,14,15):
    for per in (68,95,99):
        hist = ROOT.TH1D("2013_12_%d_%d"%(day,per),"fig_1_%d_%d"%(day,per),24,-1,24)
        #print("for : %d, %d"%(day,per))
        f = open("centerdata.csv",'r')
        r = csv.reader(f,delimiter=',')
        for p in r :
            hour = int(p[1])
            pers = int(p[2])
            rads = float(p[3])
            #print("out:%d,%d,%s"%(day,per,p[0]))
            if p[0] == "2013-12-%d"%(day) :
                if pers == per :
                    hist.Fill(hour,rads)
                    if hour == 0:
                        print("inner:%d,%d,%d,%f"%(day,per,hour,rads))

        hist.Write()
        hist.Clear()

output.Close()

