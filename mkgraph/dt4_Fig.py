import ROOT
import csv

output = ROOT.TFile("under_d_t.root","UPDATE")

f = open("d4_fig.csv",'r')

r = csv.reader(f,delimiter=',')

#t = ROOT.TTree("Tree_name","Tree_title")
#t.ReadFile("d-overhangd.dat","",',')

distance_hist = ROOT.TH1F("fig_4_1","distance",10000,900,40000)
time_hist = ROOT.TH1F("fig_4_2","time",400,0,4000)
#totl_hist_hang  = ROOT.TH1F("fig_4_2","time",10000,0,1000000)
total = 39576853
per = 100/float(total)
print(per)

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
