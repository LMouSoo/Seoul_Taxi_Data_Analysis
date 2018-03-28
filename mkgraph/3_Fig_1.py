import ROOT
import csv

output = ROOT.TFile("f_real_paris.root","UPDATE")

f = open("d-overhangd_paris.csv",'r')

r = csv.reader(f,delimiter=',')

#t = ROOT.TTree("Tree_name","Tree_title")
#t.ReadFile("d-overhangd.dat","",',')

totl_hist_dstn  = ROOT.TH2F("fig_4_1","totl_dstn",10000,0,1000000,10000,0,1000000)
totl_hist_hang  = ROOT.TH2F("fig_4_2","hang_over",10000,0,1000000,10000,0,1000000)

for p in r :
    dest = float(p[3])
    totl = float(p[0])
    hang = float(p[1])

    totl_hist_dstn.Fill(dest,totl)
    totl_hist_hang.Fill(dest,hang)


totl_hist_dstn.Write()
totl_hist_hang.Write()

output.Close()
