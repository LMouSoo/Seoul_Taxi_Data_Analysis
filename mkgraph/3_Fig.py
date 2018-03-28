import ROOT
import csv

output = ROOT.TFile("f_real2.root","UPDATE")

f = open("d-overhangd.csv",'r')

r = csv.reader(f,delimiter=',')

#t = ROOT.TTree("Tree_name","Tree_title")
#t.ReadFile("d-overhangd.dat","",',')

totl_hist_dstn  = ROOT.TH2F("fig_3_1","totl_dstn",10000,0,1000000,10000,0,1000000)
totl_hist_hang  = ROOT.TH2F("fig_3_2","hang_over",10000,0,1000000,10000,0,1000000)
i2017_hist_dstn = ROOT.TH2F("fig_3_3","2017_totl_dstn",10000,0,1000000,10000,0,1000000)
i2017_hist_hang = ROOT.TH2F("fig_3_4","2017_hang_over",10000,0,1000000,10000,0,1000000)
i2013_hist_dstn = ROOT.TH2F("fig_3_5","2013_totl_dstn",10000,0,1000000,10000,0,1000000)
i2013_hist_hang = ROOT.TH2F("fig_3_6","2013_hang_over",10000,0,1000000,10000,0,1000000)

for p in r :
    dest = float(p[3])
    totl = float(p[0])
    hang = float(p[1])
    year = int(p[4][0:5])

    totl_hist_dstn.Fill(dest,totl)
    totl_hist_hang.Fill(dest,hang)

    if year==2013 :
        i2013_hist_dstn.Fill(dest,totl)
        i2013_hist_hang.Fill(dest,hang)

    if year==2017 :
        i2017_hist_dstn.Fill(dest,totl)
        i2017_hist_hang.Fill(dest,hang)



totl_hist_dstn.Write()
totl_hist_hang.Write()
i2017_hist_dstn.Write()
i2017_hist_hang.Write()
i2013_hist_dstn.Write()
i2013_hist_hang.Write()

output.Close()
