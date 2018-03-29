import ROOT
import csv

output = ROOT.TFile("../dat/root/r5_fig.root","UPDATE")

f = open("../dat/csv/d5_fig_d_3.csv",'r')

r = csv.reader(f,delimiter=',')

hist = ROOT.TH1F("fig_5_3","3km",100000,2000,50000)

for p in r :
    distance = float(p[0])
    time = float(p[1])
    if distance > 3000.1 :
        hist.Fill(distance,1)


hist.Write()

output.Close()
