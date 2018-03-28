import ROOT
import csv

output = ROOT.TFile("r7_fig_100km.root","UPDATE")

f = open("d7_fig_100km.csv",'r')

r = csv.reader(f,delimiter=',')

#t = ROOT.TTree("Tree_name","Tree_title")
#t.ReadFile("d-overhangd.dat","",',')

rms_hist = ROOT.TH2F("fig_7","RMS",10000,0,100000,10000,0,1000000)

for p in r :
#    dest = float(p[3])
    d = float(p[0])
    h = float(p[1])
#    hang = float(p[1])

    #if distance > 10 :
    rms_hist.Fill(d,h)



rms_hist.Write()

output.Close()
