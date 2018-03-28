import ROOT
import csv

output = ROOT.TFile("r7_fig.root","UPDATE")

f = open("d7_fig.csv",'r')

r = csv.reader(f,delimiter=',')


hist = ROOT.TH1F("fig_5_3","3km",10000,0,1000)

for p in r :
    distance = float(p[0])
    time = float(p[1])

    distance_hist.Fill(distance,per)
    time_hist.Fill(time,per)


distance_hist.Write()
time_hist.Write()

output.Close()
