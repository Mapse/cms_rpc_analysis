# -*- coding: utf-8 -*-					#per poter usare caratteri speciali come _

##### script comparazione 2 scans con fit

#librerie pyROOT per disegnare grafici

import ROOT
from ROOT import gROOT
from ROOT import TCanvas, TGraph, gPad, TH1, TH2, TF1, kRed, TMultiGraph, TLegend, gStyle, TPaveStats, TStyle, TText, TList, TLatex, TGraphErrors, TMath, TFile, TMarker
from array import array
import math
import string
from datetime import datetime								#importa la libreria tempo
import time
import glob
import numpy

import config

space= "	"
newline= " \n"
#_v2 prototypes 17 (aggiunta prototipi 2017)

print "Script per plottare argon scan. ASSICURARSI DI AVER INSERITO TIPO GAP, TITOLO, E COLONNE FILE DA DISEGNARE"
print "VERSIONE 2, produce oltre a 1file+1plot per ogni gap, anche un file finale con i valori di tutte e 3 le gaps insieme /n"

scan_id = config.scan_id  

chamber_name= config.chambers.keys()[0]
gaps= config.chambers.values()[0]	
			
def resistivity(chamber):

	title_plot= chamber +" (#"+ scan_id + ")"

	S = gaps[chamber]
	L = config.thick * 2
	
	



#################### PRENDE DATI DA ROOT FILE E LI METTE IN LISTA

	nome_file_estratti=title_plot + "_data-from-ROOTfile.csv"       #nome per creare file output contenente file stratti da root file (x leggerlo dopo x plot)

	file_dati_estratti=open(nome_file_estratti, "w")		#crea file contente correnti estratte da file root

	intestaz= "HVeff_"+chamber + space + "densityIMon_"+ chamber +space + "densityIMon_err_"+ chamber + newline  #crea intestazione file con correnti estratte

	file_dati_estratti.write(intestaz)			         #scrive intestazione



	list_file= glob.glob(config.files_path + scan_id +'/*_CAEN.root')	 #mette in una lista tutti i file della directory aventi estensione .root


	list_HV=[]						#lista dove mettere i parametri estratti dai root file
	list_Imon=[]						
	list_Imon_err=[]

	for file_in in list_file:
		input_root = TFile(file_in)

		histoHV_eff = input_root.Get("HVeff_" + chamber_name + '-' + chamber)      #assegna l'istogramma preso dal root file all'istogramma nuovo histoHV_eff
		HV_eff= histoHV_eff.GetMean()
		list_HV.append(HV_eff)
	

		histoImon = input_root.Get("Imon_" + chamber_name + '-' + chamber)
		Imon= histoImon.GetMean()/S					#divide la corrente x S perchè nei root file è presa la I e non la density
		Imon_err= histoImon.GetRMS()/S
		list_Imon.append(Imon)
		list_Imon_err.append(Imon_err)
	


	point= len(list_HV)				#conta elementi in lista per creare array di queste dimensioni  (array per riordinare valori)

	matrix= numpy.empty([point,3])		#crea matrice di n righe quanti i valori di HV, e di 3 colonne: HV,ADC, ADCerr


	n=0					#indice incremento, per andarea vanti nello scorrere della lista nel ciclo for seguente

	for value in list_HV:						#mette valori da liste in matrice
		matrix[n][0]= list_HV[n]
		matrix[n][1]= list_Imon[n]
		matrix[n][2]= list_Imon_err[n]
		n=n+1


	matrix=sorted(matrix, key=lambda colonna: colonna[0])		#riordina dati da HV basse ad alte



	index=0								#indice per mettere dati da matrice in file
	for line in matrix:
		riga= str(matrix[index][0]) + space + str(matrix[index][1]) + space + str(matrix[index][2])+ newline
		file_dati_estratti.write(riga)
		index=index+1

	file_dati_estratti.close()			#chiude file dati per poterlo leggere dopo per plottare


#############PLOT

	nome_out= title_plot+ "Resistivity.csv"				#nome file uscita	

	file_output=open(nome_out, "w")				#crea file uscita contente parametri 

	intestazione= "#scan_id slope offset HV_ONset_(V) Resistance_(Ohm) Resistivity_(Ohm.cm) \n"   #crea intestazione file output

	file_output.write(intestazione)


#########

	canvas = TCanvas("canvas","canvas", 1366, 725)			#crea canvas e la nomina

	gStyle.SetErrorX(0)

	gPad.SetGrid()

	gPad.SetBottomMargin(0.12)
	gPad.SetTopMargin(0.15)						# setta margini inferiore e supreriore della 1 pad
	gPad.SetLeftMargin(0.11) 
	gPad.SetRightMargin(0.025)						# setta margini sinistro e destro della 1 pad


	gr= TMultiGraph()

	gr.SetTitle(title_plot) 							#setta titolo plot


	gStyle.SetOptFit()					#prende tutti i valori statistici del fit
	gStyle.SetStatX(0)				#imposto valori a zero per non far comparire il box, verrà prodotto box personalizzato
	gStyle.SetStatY(0)
	gStyle.SetStatH(0)
	gStyle.SetStatW(0)


################# 1 plot



	gr1 = TGraphErrors(nome_file_estratti, "%lg %lg %lg")
	gr1.SetMarkerStyle(8)
	gr1.SetMarkerSize(1.2)
	gr1.SetMarkerColor(4)
	gr1.SetLineColor(4)

	gr1.Fit("pol1","","", config.range_gr1[0], config.range_gr1[1])	       #fit da 3000-6000 anche linea fit è nell'intervallo quindi si disegna altra linea in intrevallo + grande

	fit1= gr1.GetFunction("pol1")		#si prende valori fit per disegnare linea uguale a fit ma piu lunga
	fit1.SetLineColor(0)
	fit1.SetLineWidth(0)


	p0=fit1.GetParameter(0)
	p1=fit1.GetParameter(1)


	f1= TF1 ("f1", "pol1", config.range_gr2[0], config.range_gr2[1])		#linea uguale a fit ma piu lunga
	f1.SetParameters(p0, p1)
	f1.SetLineColor(2)
	f1.SetLineWidth(3)
	f1.SetLineStyle(2)

	R1= ((1/p1)*10**6)/S				#si moltiplica per 10^6 perche la corrente è presa in micro (altrimensi si ha microohm)
	R1math= '{:.3e}'.format(R1)			#si divide per superficie perchè corrente considerata è densità di I, e dividendo si ottine I


	rho1= (R1*S)/L
	rho1math= '{:.3e}'.format(rho1)

	gr1.Draw("APN")




################# 2 plot per 2 fit (parte con valori prossimi a zero)


	
	gr2 = TGraphErrors(nome_file_estratti, "%lg %lg %lg")

										
	gr2.SetMarkerStyle(8)
	gr2.SetMarkerSize(1.2)
	gr2.SetMarkerColor(4)
	gr2.SetLineColor(4)

	gr2.Fit("pol1","","",0, config.HV_start)	       #fit da 3000-6000 anche linea fit è nell'intervallo quindi si disegna altra linea in intrevallo + grande

	fit2= gr2.GetFunction("pol1")		#si prende valori fit per disegnare linea uguale a fit ma piu lunga
	fit2.SetLineColor(0)
	fit2.SetLineWidth(0)
	

	par0=fit2.GetParameter(0)
	par1=fit2.GetParameter(1)


	f2= TF1 ("f1", "pol1", 0, config.parameter)		#linea uguale a fit ma piu lunga
	f2.SetParameters(par0, par1)
	f2.SetLineColor(2)
	f2.SetLineWidth(3)
	f2.SetLineStyle(2)

	gr2.Draw("APN")




############# multi

	gr.Add(gr1)
	#gr.Add(gr2)

	gr.Draw("APN")

	gr.GetXaxis().SetTitle("HV_{eff} [V]") 
	gr.GetYaxis().SetTitle("Density Current [#muA/cm^{2}]")				# setta nome assi
	gr.GetXaxis().SetTitleSize(0.04) 
	gr.GetYaxis().SetTitleSize(0.04)						# setta dimensione titolo assi
	gr.GetXaxis().CenterTitle()
	gr.GetYaxis().CenterTitle()							# setta posizione label assi
	gr.GetXaxis().SetTitleOffset(1.5) 
	gr.GetYaxis().SetTitleOffset(1.5)						# setta distanza titolo asse dall'asse

	gr.GetXaxis().SetNdivisions(20,5,0)

	gr.GetXaxis().SetLimits(1100,2000) 				# sett range X
	gr.SetMinimum(0.)
	#gr.SetMaximum(limitesup_y)							# setta range asse Y (metodo diverso che per le X)

	gr.GetXaxis().SetLabelSize(0.03)
	gr.GetYaxis().SetLabelSize(0.03)						# setta dimensioni label assi
	gr.GetXaxis().SetLabelOffset(0.005)
	gr.GetYaxis().SetLabelOffset(.015)						# setta distanza label(etichette linee) dall'asse


	f1.Draw('LSAME')
	f2.Draw('LSAME')


######## onset point, TROVA PUNTO INTERSEZIONE 2 RETTE FIT ( punto intersezione y1=y2)
	

	zero= par0-p0
	uno= p1-par1
	ONset= zero/uno
	ONset_format= '{:.2f}'.format(ONset)			#formatta numero con solo 2 numeri dopo virgola

	y= p0+ ONset*p1						#y del punto offset


	m= TMarker ( ONset, y, 8)				#punto di onset coordinate y e x e tipo marker 8
	m.SetMarkerSize(1.5)
	m.SetMarkerColor(2)
	m.Draw()						#disegna punto offset
	
################ statistic
# si disegna box statistiche aggiungendo titolo, cambiando colore, dimensione testo ecc

###stat

	stats1 = gr1.GetListOfFunctions().FindObject("stats").Clone("stats1")		#si prendono statistiche dal box e si crea personalizzato
	stats1.SetY1NDC(.83)								#posizione nuovo box
	stats1.SetY2NDC(.63)
	stats1.SetX1NDC(.15)
	stats1.SetX2NDC(.30)
	#stats1.SetTextColor(4)
	#stats1.SetTextSize(0.03)				#dimensione testo tutto box compreso successivo titolo

	lista1 = stats1.GetListOfLines()					#si prende statistiche nuovo box per aggiungere titolo o altre linee
	
	ONsetlet="HV ONset           "+ONset_format +" V" 
	ONset_box = TLatex(0,0,ONsetlet);					#si crea testo da aggiungere
	ONset_box.SetTextFont(42);						#personalizzazione testo da aggiungere
	ONset_box.SetTextSize(100);
	#ONset_box.SetTextColor(4);						#dovrebbe modificare dimensioni solo titolo... (non lo fa??)
	lista1.Add(ONset_box); 						#si aggiunge alla lista del box il nuovo testo


	R1let="R           "+R1math +" #Omega" 
	R1_box = TLatex(0,0,R1let);					#si crea testo da aggiungere
	R1_box.SetTextFont(42);						#personalizzazione testo da aggiungere
	R1_box.SetTextSize(100);
	#R1_box.SetTextColor(4);						#dovrebbe modificare dimensioni solo titolo... (non lo fa??)
	lista1.Add(R1_box); 						#si aggiunge alla lista del box il nuovo testo

	rho1let= "#rho       " + rho1math + " #Omegacm"
	rho1_box = TLatex(0,0,rho1let);					#si crea testo da aggiungere
	rho1_box.SetTextFont(42);						#personalizzazione testo da aggiungere
	rho1_box.SetTextSize(100);
	#rho1_box.SetTextColor(4);						#dovrebbe modificare dimensioni solo titolo... (non lo fa??)
	lista1.Add(rho1_box); 						#si aggiunge alla lista del box il nuovo testo

	stats1.Draw()								#disegna nuovo box

##########

	canvas.Update()

	nome_plot= title_plot+ ".png"
	canvas.SaveAs(nome_plot)

####################################

	#riga_dati=scan_id + space + str(p1) + space + str(p0) + space + str(ONset) + space + str(R1math) +space +str(rho1math) + newline

	#file_output.write(riga_dati)

	print "END ANALISI ", chamber
	

	#aggiunta versione 2 per file finale comprensiovo dei valori di tutte e 3 le gap
	#riga_out_3= space + str(ONset) + space + str(R1math) +space +str(rho1math)+space	    #inizia con space pechè prima messo ID senza space
	#file_finale.write(riga_out_3)


################# FINE FUNZIONE

#####USO DELLA FUNZIONE

for gap in gaps.keys():
	resistivity(gap)



print "+++++++++++++ END ++++++++++++"
