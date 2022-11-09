"""
Module designed by Ivan Cambon Bouzas 
PhD student at Instituto Galego de Fisica de Altas Enerxias (IGFAE)
This module includes functions that are thought as shortcuts for the RooFit plotting result process
Any doubt or suggestion, check https://github.com/Icambonb or 
"""

from ROOT import *
import numpy as np

"""
Basic function for plotting a histogram Roofit into a TCanvas object
-var: RooFit variable
-model: RooFit model
-dh: RooFit histogram
-bool_comp: Python bool
-comp: Python List whose components are RooFit pdf
-colors: Python List whose components are TColor objects
-xlabel: Python String for xlabel
-ylabel: Python String for ylabel
-title: Python String for title
"""

def modelplot(var,model,dh,bool_comp,comp,colors,xlabel,ylabel,title):
 fr=var.frame()
 dh.plotOn(fr)
 if bool_comp:
  for i in range(len(comp)):
  # model.plotOn(fr,RooFit.Name(comp[i]),RooFit.Components(comp[i]),RooFit.LineStyle(kDashed),RooFit.LineColor(colors[i]))
   model.plotOn(fr,RooFit.Name(comp[i]),RooFit.Components(comp[i]),RooFit.LineColor(colors[i]))
 model.plotOn(fr)
 fr.GetXaxis().SetTitle(xlabel)
 fr.GetYaxis().SetTitle(ylabel)
 fr.SetTitle(title)
 fr.Draw()
 print("chi2/bins",fr.chiSquare())

"""
Fuction that plots the Pull [(x-mean)/error] histogram of a fit. 
Designed for TCanvas objects with two TPad in horizontal position
-var: RooFit variable
-model: RooFit model
-dh: RooFit histogram
"""

def pullplot(var,model,dh):
 fr1=var.frame()
 dh.plotOn(fr1)
 model.plotOn(fr1)
 histo_pulls=fr1.pullHist()
 histo_pulls.SetFillColor(kBlack)
 histo_pulls.SetLineWidth(0)
 histo_pulls.SetMarkerSize(0)
 fr2=var.frame()
 fr2.addPlotable(histo_pulls,"B")
 fr2.SetTitle("")
 fr2.GetXaxis().SetTitle("")
 fr2.GetXaxis().SetLabelSize(0)
 fr2.GetYaxis().SetNdivisions(5)
 fr2.GetYaxis().SetLabelSize(0.2)
 fr2.GetYaxis().SetTitleSize(0.3)
 fr2.GetYaxis().SetTitleOffset(0.2)
 fr2.GetYaxis().SetTitle("Pulls")
 fr2.Draw()


"""
Function that saves or returns the parameter values of a RooFit
-par: List with RooFit variables
-par_names: List with strs which corresponds to RooFit variables
-model: RooFit model
-dh: RooFit histogram
-archive_name: str for archive name
-save_bool: Python bool
"""

def parameter_saving(par,par_names,model,dh,archive_name,save_bool):
 par_vals=[par[i].getVal() for i in range(len(par))]
 par_unc=[par[i].getError() for i in range(len(par))]

 Chi2_model=RooChi2Var("chi2","chi2",model,dh)
 Chi2_val=Chi2_model.getVal()
 par_vals.append(Chi2_val)
 par_names_un=list(par_names)

 par_names.append("chi2")
 vals_order='order: ';unc_order='order: '

 for i in range(len(par_names)):
  vals_order=vals_order+par_names[i]+' '
 for i in range(len(par_names_un)):
  unc_order=unc_order+par_names_un[i]+' '

 if save_bool:
  np.savetxt(archive_name+'_vals.txt',par_vals,header=vals_order)
  np.savetxt(archive_name+'_unc.txt',par_unc,header=unc_order)
 else:
  return par_vals,par_unc



"""
Function that returns in terminal the fit interesting results.
-r: Fit result object
"""

def fit_result(r):
 print("EDM=",r.edm())
 print("-log(L) minimum=", r.minNll())
 print("final value of floating parameters")
 r.floatParsFinal().Print("s")

 cor=r.correlationMatrix()
 cov=r.covarianceMatrix()

 print("correlation matrix")
 cor.Print()
 print("covariance matrix")
 cov.Print()
 
 

"""
Function that plots the covariance ellipse of two fit parameters
-r: Fit result object
-par1: RooRealVar object. Must be a free parameter of the fit model
-par2: RooRealVar object. Must be a free parameter of the fit model
-name1: str that corresponds to par1
-name2: str that corresponds to par2
-n: float object. Defines the limit of the plot. Multiplies the error values
"""

def MatrixCov_2D(r,par1,par2,name1,name2,n):
 val1=par1.getVal()
 val2=par2.getVal()

 u1=par1.getError()
 u2=par2.getError()

 frame=RooPlot(par1,par2,(val1-n*u1),(val1+n*u1),(val2-n*u2),(val2+n*u2))
 frame.SetTitle("Covariance between"+" "+name1+" "+"and"+" "+name2)
 r.plotOn(frame, par1, par2, "ME12ABHV")
 frame.Draw()

 
"""
Function that gives the correlation between two parameters. A option for correlation matrix 2D plot is set
-r: Fit result object
-par1: RooRealVar object. Must be a free parameter of the fit model
-par2: RooRealVar object. Must be a free parameter of the fit model
-name1: str that corresponds to par1
-name2: str that corresponds to par2
-Bool: bool object. If it is True, the 2D matrix is plotted in a TCanvas 
"""

def MatrixCorr_vals(r,par1,par2,name1,name2,Bool):
 print("Correlation between"+" "+name1+" "+"and"+" "+name2, r.correlation(par1,par2))
 
 if Bool: 
  hcorr = r.correlationHist()
  hcorr.Draw("colz")







