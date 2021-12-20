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

spazio= "	"
newline= " \n"

chambers = config.chambers

scan_list = config.scan_list

lenged_list_bot = config.lenged_list_bot
lenged_list_top = config.lenged_list_top	

files_path = config.files_path

for chamber in chambers:
	
	index_scan=0								
	
	#if chamber== "KODELD":
	S=1 
		
	
	numero_scan= len(scan_list)	
	graph_list=[]						
	graph_list_TOP=[]
	graph_list_BOT=[]
	graph_index=1						
	for scan_in in range(1,numero_scan+1):			
            graph_list.append("gr"+str(graph_index))	#gr1, gr2, gr3...
            graph_list_TOP.append("gr"+str(graph_index))
            graph_list_BOT.append("gr"+str(graph_index))
            graph_index=graph_index+1			#incrementa indice grafico (1,2,3..)
	 	
			
	######################### CREA CANVAS E MULTIGRAPH COMUNE DOVE AGGIUNGERE TUTTI GRAFICI
			
	canvas = TCanvas("canvas","canvas", 600, 600)			
			
	gPad.SetGrid()
			
	gPad.SetBottomMargin(0.1)
	gPad.SetTopMargin(0.12)						
	gPad.SetLeftMargin(0.15) 
	gPad.SetRightMargin(0.025)						
			
	gStyle.SetOptFit()					
	gStyle.SetStatX(0)					
	gStyle.SetStatY(0)
	gStyle.SetStatH(0)
	gStyle.SetStatW(0)
		
	gStyle.SetErrorX(0)
			
	gPad.SetGrid()
			
	gr= TMultiGraph()
	gr_TOP= TMultiGraph()
	gr_BOT= TMultiGraph()
    #gr_4 = TMultiGraph()
			
	#loop per ogni scan da analizzare
	color_index=1
	marker_index=20
	print "Processing..."
		
	for scan in scan_list:
		
		#loop per prendere file root
		list_rootfile= glob.glob(files_path +scan+'/*_CAEN.root')  
					
		#if chamber == "KODELD":
					
		list_HV=array('f')					#lista dove mettere i parametri estratti dai root file
		list_Imon=array('f')						
		list_Imon_err=array('f')
		list_Imon_TOP=array('f')
		list_Imon_BOT=array('f')
		list_Imon_TOP_err=array('f')
		list_Imon_BOT_err=array('f')
					
		
		for file_in in list_rootfile:				#LOOP PER OGNI ROOT FILE
			input_root = TFile(file_in)		#apre root file CAEN
						
			#if chamber=="KodelD":

			for gaps in chambers[chamber]:
				if gaps.startswith('BOT'):
					bot_gap_name = gaps
				elif gaps.startswith('TOP'):
					top_gap_name = gaps

			
			histoHV_eff_BOT = input_root.Get("HVeff_" + chamber + '-' + bot_gap_name)    #assegna histogramm preso da rootfile a histogramma nuovo histoHV_eff

			HV_eff_BOT= histoHV_eff_BOT.GetMean()
			
			
			histoImon_BOT = input_root.Get("Imon_" + chamber + '-'  + bot_gap_name)
			Imon_BOT= histoImon_BOT.GetMean()	#divide la corrente x S perchè nei root file è presa la I e non la density
			Imon_err_BOT= histoImon_BOT.GetRMS()
			
			
			histoHV_eff_TOP = input_root.Get("HVeff_" + chamber + '-' + top_gap_name)    #assegna histogramm preso da rootfile a histogramma nuovo histoHV_eff
			HV_eff_TOP= histoHV_eff_TOP.GetMean()
			
			
			histoImon_TOP = input_root.Get("Imon_" + chamber + '-' + top_gap_name)
			Imon_TOP= histoImon_TOP.GetMean()	#divide la corrente x S perchè nei root file è presa la I e non la density
			Imon_err_TOP= histoImon_TOP.GetRMS()							
								
			Imon_TOT= ((Imon_BOT)+(Imon_TOP))
			Imon_TOT_err=((Imon_err_BOT)+(Imon_err_TOP))
								
								
		# AGGIUNGE HV, E IMON A LISTE MEAN VALUES
		
			list_HV.append(HV_eff_BOT)		
			list_Imon.append(Imon_TOT)
			list_Imon_err.append(Imon_TOT_err)
			list_Imon_TOP.append(Imon_TOP/S)
			list_Imon_BOT.append(Imon_BOT/S)
			list_Imon_TOP_err.append(Imon_err_TOP)
			list_Imon_BOT_err.append(Imon_err_BOT)
			
								
	######### PLOT
								
		#plot						
		np= len(list_HV)		#conta numero punti per input graph
									
		#if chamber == "KODELC" or chamber == "KodelGIF3":
								
		graph_list[index_scan] = TGraphErrors(np,list_HV,list_Imon,list_Imon_err)
		graph_list_TOP[index_scan] = TGraphErrors(np,list_HV,list_Imon_TOP,list_Imon_TOP_err)
		graph_list_BOT[index_scan] = TGraphErrors(np,list_HV,list_Imon_BOT,list_Imon_BOT_err)
									
									
		ROOT.TGaxis.SetMaxDigits(6)
		graph_list[index_scan].SetTitle(chamber+"_TOT")
								
		graph_list[index_scan].GetXaxis().SetTitle("HV_{eff} [V]") 
		graph_list[index_scan].GetYaxis().SetTitle("Current [#muA/cm^2]")				
									
		graph_list[index_scan].GetXaxis().SetTitleSize(0.04) 
		graph_list[index_scan].GetYaxis().SetTitleSize(0.04)				
		graph_list[index_scan].GetXaxis().CenterTitle()
		graph_list[index_scan].GetYaxis().CenterTitle()					
		graph_list[index_scan].GetXaxis().SetTitleOffset(1.0) 
		graph_list[index_scan].GetYaxis().SetTitleOffset(2.5)			
									
		graph_list[index_scan].GetXaxis().SetLabelSize(0.03)
		graph_list[index_scan].GetYaxis().SetLabelSize(0.03)				
		graph_list[index_scan].GetXaxis().SetLabelOffset(0.005)
		graph_list[index_scan].GetYaxis().SetLabelOffset(.015)		
									
		graph_list[index_scan].SetMarkerStyle(marker_index)
		graph_list[index_scan].SetMarkerSize(1.2)
		graph_list[index_scan].SetMarkerColor(color_index)
		graph_list[index_scan].SetLineColor(color_index)
									
		graph_list[index_scan].Draw('APE')
									
		gr.Add(graph_list[index_scan])
	
		graph_list_TOP[index_scan].SetTitle(chamber+"_TOP")
		graph_list_TOP[index_scan].GetXaxis().SetTitle("HV_{eff} [V]")
		graph_list_TOP[index_scan].GetYaxis().SetTitle("Current [#muA/cm^2]")
		graph_list_TOP[index_scan].GetXaxis().SetTitleSize(0.04)
		graph_list_TOP[index_scan].GetYaxis().SetTitleSize(0.04)
		graph_list_TOP[index_scan].GetXaxis().CenterTitle()
		graph_list_TOP[index_scan].GetYaxis().CenterTitle()
		graph_list_TOP[index_scan].GetXaxis().SetTitleOffset(1.0)
		graph_list_TOP[index_scan].GetYaxis().SetTitleOffset(2.5)
		graph_list_TOP[index_scan].GetXaxis().SetLabelSize(0.03)
		graph_list_TOP[index_scan].GetYaxis().SetLabelSize(0.03)
		graph_list_TOP[index_scan].GetXaxis().SetLabelOffset(0.005)
		graph_list_TOP[index_scan].GetYaxis().SetLabelOffset(.015)
		graph_list_TOP[index_scan].SetMarkerStyle(marker_index)
		graph_list_TOP[index_scan].SetMarkerSize(1.2)
		graph_list_TOP[index_scan].SetMarkerColor(color_index)
		graph_list_TOP[index_scan].SetLineColor(color_index)
		graph_list_TOP[index_scan].Draw('APE')
		gr_TOP.Add(graph_list_TOP[index_scan])
        
		graph_list_BOT[index_scan].SetTitle(chamber+"_BOT")
		graph_list_BOT[index_scan].GetXaxis().SetTitle("HV_{eff} [V]")
		graph_list_BOT[index_scan].GetYaxis().SetTitle("Current [#muA]")
		graph_list_BOT[index_scan].GetXaxis().SetTitleSize(0.04)
		graph_list_BOT[index_scan].GetYaxis().SetTitleSize(0.04)
		graph_list_BOT[index_scan].GetXaxis().CenterTitle()
		graph_list_BOT[index_scan].GetYaxis().CenterTitle()
		graph_list_BOT[index_scan].GetXaxis().SetTitleOffset(1.0)
		graph_list_BOT[index_scan].GetYaxis().SetTitleOffset(2.5)
		graph_list_BOT[index_scan].GetXaxis().SetLabelSize(0.03)
		graph_list_BOT[index_scan].GetYaxis().SetLabelSize(0.03)
		graph_list_BOT[index_scan].GetXaxis().SetLabelOffset(0.005)
		graph_list_BOT[index_scan].GetYaxis().SetLabelOffset(.015)
		graph_list_BOT[index_scan].SetMarkerStyle(marker_index)
		graph_list_BOT[index_scan].SetMarkerSize(1.2)
		graph_list_BOT[index_scan].SetMarkerColor(color_index)
		graph_list_BOT[index_scan].SetLineColor(color_index)
		graph_list_BOT[index_scan].Draw('APE')
		gr_BOT.Add(graph_list_BOT[index_scan])
			
			
		#fine analisi scan
			
		marker_index=marker_index+1
		color_index=color_index+1
		if color_index == 10 or color_index == 5:			#aumenta di 1 per non usare colore 10 che corrisponde al bianco
			color_index=color_index+1
			
		index_scan=index_scan+1
									
										
	############ MODIFICHE MULTIGRAPH E SALVATAGGIO PLOT
										
	print "Producing canvas..."											
										
	## Legend - BOT
	leg_bot = ROOT.TLegend(.2, 0.5, .6, .85)
	leg_bot.SetBorderSize(0)
	leg_bot.SetFillStyle(0)
	leg_bot.SetTextSize(0.03)
       										
	legend_index=0 
	for n_legend in lenged_list_bot:
		leg_bot.AddEntry(graph_list[legend_index], lenged_list_bot[legend_index], "lp")
		legend_index=legend_index+1
	leg_bot.Draw()
			

	gr_BOT.Draw("APE")										
	gr_BOT.SetTitle(chamber+"_BOT")										
	gr_BOT.GetXaxis().SetTitle("HV_{eff} [V]") 
	gr_BOT.GetYaxis().SetTitle("Current [#muA]")
	gr_BOT.GetXaxis().SetTitleSize(0.04) 
	gr_BOT.GetYaxis().SetTitleSize(0.04)						
	gr_BOT.GetXaxis().CenterTitle()
	gr_BOT.GetYaxis().CenterTitle()							
	gr_BOT.GetXaxis().SetTitleOffset(1.2)                                               	
	gr_BOT.GetXaxis().SetLabelSize(0.03)
	gr_BOT.GetYaxis().SetLabelSize(0.03)					
	gr_BOT.GetXaxis().SetLabelOffset(0.005)
	gr_BOT.GetYaxis().SetLabelOffset(.015)		 		
	gPad.Update()
	gPad.Modified()
	leg_bot.Draw()
	
	canvas.Update()
	plot_name= chamber+"_CurrentBOT.png"		
	canvas.SaveAs(plot_name)

	## Legend - TOP
	leg_top = ROOT.TLegend(.2, 0.5, .6, .85)
	leg_top.SetBorderSize(0)
	leg_top.SetFillStyle(0)
	leg_top.SetTextSize(0.03)
       										
	legend_index=0 
	for n_legend in lenged_list_top:
		leg_top.AddEntry(graph_list[legend_index], lenged_list_top[legend_index], "lp")
		legend_index=legend_index+1
	leg_top.Draw()

	gr_TOP.Draw("APE")										
	gr_TOP.SetTitle(chamber+"_TOP")										
	gr_TOP.GetXaxis().SetTitle("HV_{eff} [V]") 
	gr_TOP.GetYaxis().SetTitle("Current [#muA]")
	gr_TOP.GetXaxis().SetTitleSize(0.04) 
	gr_TOP.GetYaxis().SetTitleSize(0.04)						
	gr_TOP.GetXaxis().CenterTitle()
	gr_TOP.GetYaxis().CenterTitle()							
	gr_TOP.GetXaxis().SetTitleOffset(1.2)                                               	
	gr_TOP.GetXaxis().SetLabelSize(0.03)
	gr_TOP.GetYaxis().SetLabelSize(0.03)					
	gr_TOP.GetXaxis().SetLabelOffset(0.005)
	gr_TOP.GetYaxis().SetLabelOffset(.015)		 		
	gPad.Update()
	gPad.Modified()
	leg_top.Draw()
	
	canvas.Update()
	plot_name= chamber+"_CurrentTOP.png"		
	canvas.SaveAs(plot_name)
	
	
	
					

