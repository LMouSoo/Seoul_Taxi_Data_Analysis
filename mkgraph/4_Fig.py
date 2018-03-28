import ROOT
import csv

output = ROOT.TFile("r7_fig.root","UPDATE")

f = open("d7_fig.csv",'r')

r = csv.reader(f,delimiter=',')

#t = ROOT.TTree("Tree_name","Tree_title")
#t.ReadFile("d-overhangd.dat","",',')

rms_hist = ROOT.TH2F("fig_7","RMS",10000,0,1000)

for p in r :
#    dest = float(p[3])
    distance = float(p[0])
    time = float(p[1])
#    hang = float(p[1])

    #if distance > 10 :
    distance_hist.Fill(distance,per)
    time_hist.Fill(time,per)

    #totl_hist_hang.Fill(dest,hang)


distance_hist.Write()
time_hist.Write()
#totl_hist_hang.Write()

output.Close()
