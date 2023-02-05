import matplotlib.pyplot as plt
import sandwichmodel_function as SM
import numpy

greek_alphabet = {
    u'\u0391': 'Alpha',
    u'\u0392': 'Beta',
    u'\u0393': 'Gamma',
    u'\u0394': 'Delta',
    u'\u0395': 'Epsilon',
    u'\u0396': 'Zeta',
    u'\u0397': 'Eta',
    u'\u0398': 'Theta',
    u'\u0399': 'Iota',
    u'\u039A': 'Kappa',
    u'\u039B': 'Lamda',
    u'\u039C': 'Mu',
    u'\u039D': 'Nu',
    u'\u039E': 'Xi',
    u'\u039F': 'Omicron',
    u'\u03A0': 'Pi',
    u'\u03A1': 'Rho',
    u'\u03A3': 'Sigma',
    u'\u03A4': 'Tau',
    u'\u03A5': 'Upsilon',
    u'\u03A6': 'Phi',
    u'\u03A7': 'Chi',
    u'\u03A8': 'Psi',
    u'\u03A9': 'Omega',
    u'\u03B1': 'alpha',
    u'\u03B2': 'beta',
    u'\u03B3': 'gamma',
    u'\u03B4': 'delta',
    u'\u03B5': 'epsilon',
    u'\u03B6': 'zeta',
    u'\u03B7': 'eta',
    u'\u03B8': 'theta',
    u'\u03B9': 'iota',
    u'\u03BA': 'kappa',
    u'\u03BB': 'lamda',
    u'\u03BC': 'mu',
    u'\u03BD': 'nu',
    u'\u03BE': 'xi',
    u'\u03BF': 'omicron',
    u'\u03C0': 'pi',
    u'\u03C1': 'rho',
    u'\u03C3': 'sigma',
    u'\u03C4': 'tau',
    u'\u03C5': 'upsilon',
    u'\u03C6': 'phi',
    u'\u03C7': 'chi',
    u'\u03C8': 'psi',
    u'\u03C9': 'omega',
}


def cleaner(plotcc, plot):
    links = True
    rechts = True 
    k=0
    plotcc_neu =[]
    for element in plotcc:
        plotcc_neu.append("wert")
        if (k >= 0 and len(plotcc) > k+1) and ((plotcc[k] == None and plotcc[k-1] != None and plotcc[k+1] == None) or (plotcc[k] == None and plotcc[k-1] == None and plotcc[k+1] != None)):
            plotcc_neu[k] = plot[k]
        else:
            plotcc_neu[k] = plotcc[k]
        
        k+=1

    return plotcc_neu


res_dic = {
    "as_xi_bot" : {"aaa" : [1], "bbb" : [0], "xmax" : 701, "ymax" : 10000, "ylabelname" : "$a_{s,x,bot}$ [mm\u00b2/m]", "ylabelname2" : "$a_{s,\u03BE,bot}$ [mm\u00b2/m]"},
    "as_xi_top" : {"aaa" : [1], "bbb" : [1], "xmax" : 701, "ymax" : 10000, "ylabelname" : "$a_{s,x,top}$ [mm\u00b2/m]", "ylabelname2" : "$a_{s,\u03BE,top}$ [mm\u00b2/m]"},
    "as_eta_bot" : {"aaa" : [2], "bbb" : [0], "xmax" : 701, "ymax" : 10000, "ylabelname" : "$a_{s,y,bot}$ [mm\u00b2/m]", "ylabelname2" : "$a_{s,\u03B7,bot}$ [mm\u00b2/m]"},
    "as_eta_top" : {"aaa" : [2], "bbb" : [1], "xmax" : 701, "ymax" : 10000, "ylabelname" : "$a_{s,y,top}$ [mm\u00b2/m]", "ylabelname2" : "$a_{s,\u03B7,top}$ [mm\u00b2/m]"},
    "as_z" :  {"aaa" : [3], "bbb" : None, "xmax" : 701, "ymax" : 1000, "ylabelname" : "$a_{s,z}$ [mm\u00b2/m]"},
    "Fall_bot" : {"aaa" : [4], "bbb" : [0], "xmax" : 701, "ymax" : 4.2, "ylabelname" : "$Fall_{bot }$ [-]"},
    "Fall_top" : {"aaa" : [4], "bbb" : [1], "xmax" : 701, "ymax" : 4.2, "ylabelname" : "$Fall_{top }$ [-]"},
    "CC_bot" : {"aaa" : [5], "bbb" : [0], "xmax" : 701, "ymax" : 2.2, "ylabelname" : "$CC_{bot }$ [-]"},
    "CC_top" : {"aaa" : [5], "bbb" : [1], "xmax" : 701, "ymax" : 2.2, "ylabelname" : "$CC_{top }$ [-]"},
    "t_bot" : {"aaa" : [6], "bbb" : [0], "xmax" : 701, "ymax" : 150, "ylabelname" : "$t_{bot }$ [mm]"},
    "t_top" : {"aaa" : [6], "bbb" : [1], "xmax" : 701, "ymax" : 150, "ylabelname" : "$t_{top }$ [mm]"},
    "k_bot" : {"aaa" : [7], "bbb" : [0], "xmax" : 701, "ymax" : 10, "ylabelname" : "$k_{bot }$ [-]"},
    "k_top" : {"aaa" : [7], "bbb" : [1], "xmax" : 701, "ymax" : 10, "ylabelname" : "$k_{top }$ [-]"},
    "psi_bot" : {"aaa" : [8], "bbb" : [0], "xmax" : 701, "ymax" : 180, "ylabelname" : "$\u03C8_{bot }$ [°]"},
    "psi_top" : {"aaa" : [8], "bbb" : [1], "xmax" : 701, "ymax" : 180, "ylabelname" : "$\u03C8_{top }$ [°]"},
    "m_shear_c" : {"aaa" : [9], "bbb" : None, "xmax" : 701, "ymax" : 1.2, "ylabelname" : "$\u03BC_{shear,c}$ [-]"},
    "m_cc_bot" : {"aaa" : [10], "bbb" : [0], "xmax" : 701, "ymax" : 1.2, "ylabelname" : "$\u03BC_{cc,bot}$ [-]"},
    "m_cc_top" : {"aaa" : [10], "bbb" : [1], "xmax" : 701, "ymax" : 1.2, "ylabelname" : "$\u03BC_{cc,top}$ [-]"},
    "m_c_total" : {"aaa" : [11], "bbb" : None, "xmax" : 701, "ymax" : 1.2, "ylabelname" : "$\u03BC_{c,total}$ [-]"},
}

#------------------------------------------------------------------------------------------------------------------------------------------
# plottet viele charts

name = "nx"
code = "sia"
x_label  = "$n_x$ [kN/m]"

print("start")

#variabeln = ["vx", "ny", "nxy", "my", "vy", "mx", "mxy",  "h", "fck", "theta", "alpha", "spezial"]
#variabeln =  ["nx", "spezial"]
variabeln =  ["vx"]

for variabel in variabeln:
    print("var = "+ variabel)
    nx = [0, 0, 0, 0, 0]
    ny = [0, 0, 0, 0, 0]
    nxy = [0, 0, 0, 0, 0]

    mx = [0, 0, 0, 0, 0]
    my = [0, 0, 0, 0, 0]
    mxy = [0, 0, 0, 0, 0]

    vx = [0, 0, 0, 0, 0]
    vy = [0, 0, 0, 0, 0]

    h = [300, 300, 300, 300, 300]
    fck = [30, 30, 30, 30, 30]
    theta = [45, 45 ,45 ,45 ,45]
    alpha = [0, 0, 0, 0, 0]
    beta = [90, 90, 90, 90, 90]
    
    
    if variabel == "spezial":
        
        legende = ["Mindestbewehrung: True", "Druckzoneniteration: True",  "Beides: False",] #nx

    elif variabel == "nx":
        nx = [0, -2000, -1000, 1000, 2000]
        legende = ["$n_x$ = -2000 kN/m", "$n_x$ = -1000 kN/m",  "$n_x$ =  1000 kN/m", "$n_x$ =  2000 kN/m", "$n_x$ =  0 kN/m",] #nx
    
    elif variabel == "ny":
        ny = [0, -1000, -500, 500, 1000]
        legende = ["$n_y$ = -1000 kN/m", "$n_y$ = -500 kN/m",  "$n_y$ =  500 kN/m", "$n_y$ =  1000 kN/m", "$n_y$ =  0 kN/m",] #ny

    elif variabel == "nxy":
        nxy = [0, -600, -300, 300, 600]
        legende = ["$n_{xy }$ = -600 kN/m", "$n_{xy }$ = -300 kN/m",  "$n_{xy }$ =  300 kN/m", "$n_{xy }$ =  600 kN/m", "$n_{xy }$ =  0 kN/m",] #ny
    
    elif variabel == "vx":
        vx = [0, 100, 200, 300, 400]
        legende = ["$v_x$ = 100 kN/m", "$v_x$ = 200 kN/m",  "$v_x$ =  300 kN/m", "$v_x$ =  400 kN/m", "$v_x$ =  0 kN/m",] #vx
    
    elif variabel == "vy":
        vy = [0, -2000, -1000, 1000, 2000]
        legende = ["$v_y$ = -2000 kN/m", "$v_y$ = -1000 kN/m",  "$v_y$ =  1000 kN/m", "$v_y$ =  2000 kN/m", "$v_y$ =  0 kN/m",] #vy

    elif variabel == "mx":
        mx = [0, -100*1000, -50*1000, 50*1000, 100*1000]
        legende = ["$m_{x }$ = -100 kNm/m", "$m_{x }$ = -50 kNm/m",  "$m_{x }$ =  50 kNm/m", "$m_{x }$ =  100 kNm/m", "$m_{x }$ =  0 kNm/m",] 

    elif variabel == "my":
        my = [0, -100*1000, -50*1000, 50*1000, 100*1000]
        legende = ["$m_{y }$ = -100 kNm/m", "$m_{y }$ = -50 kNm/m",  "$m_{y }$ =  50 kNm/m", "$m_{y }$ =  100 kNm/m", "$m_{y }$ =  0 kNm/m",]

    elif variabel == "mxy":
        mxy = [0, -50*1000, -25*1000, 25*1000, 50*1000]
        legende = ["$m_{xy }$ = -50 kNm/m", "$m_{xy }$ = -25 kNm/m",  "$m_{xy }$ =  25 kNm/m", "$m_{xy }$ =  50 kNm/m", "$m_{xy }$ =  0 kNm/m",] 

    elif variabel == "h":
        h = [300, 200, 250, 400, 500]
        legende = ["h = 200 mm", "h = 250 mm",  "h = 400 mm", "h = 500 mm", "h = 300 mm", ] #h
    
    elif variabel == "fck":
        fck = [30, 12, 20, 40, 50]
        legende = ["C12/15", "C20/25",  "C40/50", "C50/60", "C30/37", ] #fck
    
    elif variabel == "theta":
        theta = [45, 25, 30, 35, 40 ]
        legende = ["$\u03B8_{Kern }$ = 25°", "$\u03B8_{Kern }$ = 30°",  "$\u03B8_{Kern }$ = 35°", "$\u03B8_{Kern }$ = 40°", "$\u03B8_{Kern }$ = 45°",]
    
    elif variabel == "alpha":
        alpha = [0, -30, -15, 10, 20]
        legende = ["\u03B1 = -30°", "\u03B1 = -15°",  "\u03B1 = 10°", "\u03B1 = 20°", "\u03B1 = 0°", ] #alpha
    
    schubnachweis = "sia"
    sets = [[False, False, "sia"],[False, False, "vereinfacht"],[True, False, schubnachweis]]
    setname = ["_ffs_neu", "_ffv_neu", "_tfs_FALSCH"]
    settext = ["Mindestbewehrung: Aus - Druckzoneniteration: Aus - Schubnachweis: 'sia' " , "Mindestbewehrung: Aus - Druckzoneniteration: Aus - Schubnachweis: 'vereinfacht'", "FALSCH"]
    j = 0
    for se in sets:

        print('\t' + setname[j])
        
        zusatzname = variabel + setname[j]
        j += 1
    
        resultate = list(res_dic.keys())
        Anzahl = [0,1,2,3,4]
        out = [[],[],[],[],[]]
        out_cc = [[],[],[],[],[]]
    
    
        for resultat in resultate:
            print('\t'+ '\t' + resultat)
            x = list(numpy.arange(-4000, 0, 50))


            for xx in x:
                printausnahme = False
                if variabel == "spezial":                    
                    se = [False, False, schubnachweis]
                    zusatzname = "spezial"
                    printausnahme = True   

                zahl = 0 
                inp1 = [1,mx[zahl],my[zahl],mxy[zahl],vx[zahl],vy[zahl],((vx[zahl]**2.0+vy[zahl]**2.0)**0.5),(xx),ny[zahl],nxy[zahl],h[zahl],40,40,fck[zahl],theta[zahl],435, alpha[zahl],alpha[zahl],beta[zahl],beta[zahl], se[0], se[1], se[2], code,  [1,0,0], [1,0,0],[0,1,0],[0,0,1]]

                if variabel == "spezial":
                    se = [True, False, schubnachweis]  

                zahl+=1                     
                inp2 = [2,mx[zahl],my[zahl],mxy[zahl],vx[zahl],vy[zahl],((vx[zahl]**2.0+vy[zahl]**2.0)**0.5),(xx),ny[zahl],nxy[zahl],h[zahl],40,40,fck[zahl],theta[zahl],435, alpha[zahl],alpha[zahl],beta[zahl],beta[zahl], se[0], se[1], se[2], code, [1,0,0], [1,0,0],[0,1,0],[0,0,1]]
                zahl+=1  
                inp3 = [3,mx[zahl],my[zahl],mxy[zahl],vx[zahl],vy[zahl],((vx[zahl]**2.0+vy[zahl]**2.0)**0.5),(xx),ny[zahl],nxy[zahl],h[zahl],40,40,fck[zahl],theta[zahl],435, alpha[zahl],alpha[zahl],beta[zahl],beta[zahl], se[0], se[1], se[2], code, [1,0,0], [1,0,0],[0,1,0],[0,0,1]]

                if variabel == "spezial":
                    se = [False, True, schubnachweis]    
                zahl+=1  
                inp4 = [4,mx[zahl],my[zahl],mxy[zahl],vx[zahl],vy[zahl],((vx[zahl]**2.0+vy[zahl]**2.0)**0.5),(xx),ny[zahl],nxy[zahl],h[zahl],40,40,fck[zahl],theta[zahl],435, alpha[zahl],alpha[zahl],beta[zahl],beta[zahl], se[0], se[1], se[2], code, [1,0,0], [1,0,0],[0,1,0],[0,0,1]]
                zahl+=1  
                inp5 = [5,mx[zahl],my[zahl],mxy[zahl],vx[zahl],vy[zahl],((vx[zahl]**2.0+vy[zahl]**2.0)**0.5),(xx),ny[zahl],nxy[zahl],h[zahl],40,40,fck[zahl],theta[zahl],435, alpha[zahl],alpha[zahl],beta[zahl],beta[zahl], se[0], se[1], se[2], code, [1,0,0], [1,0,0],[0,1,0],[0,0,1]]
    
                inp = [inp1,inp2,inp3,inp4,inp5]
    
                for i in Anzahl:
                
                    out[i].append(SM.Sandwichmodel(inp[i]))
    
            aaa = res_dic[resultat]["aaa"][0]
    
            if resultat == "as_z":
                bbb = res_dic[resultat]["bbb"]
    
            elif resultat == "m_shear_c":
                bbb = res_dic[resultat]["bbb"]

            elif resultat == "m_c_total":
                bbb = res_dic[resultat]["bbb"]   
            
            else:    
                bbb = res_dic[resultat]["bbb"][0]
    
            ymax = res_dic[resultat]["ymax"]
            xmax = 0

            xmin = -4000
            ymin = 0
            print(xmin)
    
    
            plot1 = []
            plot2 = []
            plot3 = []
            plot4 = []
            plot5 = []
            plotcc1 = []
            plotcc2 = []
            plotcc3 = []
            plotcc4 = []
            plotcc5 = []
    
            #print(resultat)
    
            if resultat == "as_z" or resultat == "m_shear_c" or resultat == "m_c_total":
                
                xx = 0
                for xxx in x:
                    if out[0][xx][5][0] != 2 and out[0][xx][5][1] != 2:
                        
                        plot1.append(out[0][xx][aaa])
                        plotcc1.append(None)

                    else:
                        
                        plot1.append(None)
                        plotcc1.append(out[0][xx][aaa])

    
                    if out[1][xx][5][0] != 2 and out[1][xx][5][1] != 2:
                    
                        plot2.append(out[1][xx][aaa])
                        plotcc2.append(None)
                    else:
                        plot2.append(None)
                        plotcc2.append(out[1][xx][aaa])
    
                    if out[2][xx][5][0] != 2 and out[2][xx][5][1] != 2:
                    
                        plot3.append(out[2][xx][aaa])
                        plotcc3.append(None)
                    else:
                        plot3.append(None)
                        plotcc3.append(out[2][xx][aaa])
    
                    if out[3][xx][5][0] != 2 and out[3][xx][5][1] != 2:
                    
                        plot4.append(out[3][xx][aaa])
                        plotcc4.append(None)
                    else:
                        plot4.append(None)
                        plotcc4.append(out[3][xx][aaa])
    
                    if out[4][xx][5][0] != 2 and out[4][xx][5][1] != 2:
                    
                        plot5.append(out[4][xx][aaa])
                        plotcc5.append(None)
                    else:
                        plot5.append(None)
                        plotcc5.append(out[4][xx][aaa]) 
                    xx+=1
            else:
                
                xx = 0
                for xxx in x:
                    if out[0][xx][5][0] != 2 and out[0][xx][5][1] != 2:
                        plot1.append(out[0][xx][aaa][bbb])
                        plotcc1.append(None)
                    else:
                        plot1.append(None)
                        plotcc1.append(out[0][xx][aaa][bbb])
    
                    if out[1][xx][5][0] != 2 and out[1][xx][5][1] != 2:
                        plot2.append(out[1][xx][aaa][bbb])
                        plotcc2.append(None)
                    else:
                        plot2.append(None)
                        plotcc2.append(out[1][xx][aaa][bbb])
    
                    if out[2][xx][5][0] != 2 and out[2][xx][5][1] != 2:
                        plot3.append(out[2][xx][aaa][bbb])
                        plotcc3.append(None)
                    else:
                        plot3.append(None)
                        plotcc3.append(out[2][xx][aaa][bbb])
    
                    if out[3][xx][5][0] != 2 and out[3][xx][5][1] != 2:
                        plot4.append(out[3][xx][aaa][bbb])
                        plotcc4.append(None)
                    else:
                        plot4.append(None)
                        plotcc4.append(out[3][xx][aaa][bbb])
    
                    if out[4][xx][5][0] != 2 and out[4][xx][5][1] != 2:
                        plot5.append(out[4][xx][aaa][bbb])
                        plotcc5.append(None)
                    else:
                        plot5.append(None)
                        plotcc5.append(out[4][xx][aaa][bbb])

                    xx += 1                    
                

                plotcc1 = cleaner(plotcc1,plot1)
                plotcc2 = cleaner(plotcc2,plot2)
                plotcc3 = cleaner(plotcc3,plot3)
                plotcc4 = cleaner(plotcc4,plot4)
                plotcc5 = cleaner(plotcc5,plot5)


            if (variabel == "alpha" or variabel == "beta") and (resultat == "as_xi_bot" or resultat == "as_xi_top" or resultat == "as_eta_bot" or resultat == "as_eta_top" ):
                y_label = res_dic[resultat]["ylabelname2"]

            else:
                y_label = res_dic[resultat]["ylabelname"]

            plt.xlabel(x_label)
            #plt.ylabel("$a_{s,\u03BE,bot}$ [mm\u00b2/m]") #as_xi
            plt.ylabel(y_label) #as_z

            if printausnahme == False:
                plt.plot(x,plot2, color = 'darkblue', linewidth = 1.5, linestyle="-" , Label="psi=0")
            plt.plot(x,plot3, color = 'dodgerblue', linewidth = 1.5, linestyle="-" , Label="psi=0")
            plt.plot(x,plot4, color = 'darkorange', linewidth = 1.5, linestyle="-" , Label="psi=0")
            if printausnahme == False:
                plt.plot(x,plot5, color = 'darkred', linewidth = 1.5, linestyle="-" , Label="psi=0")
    
            plt.plot(x,plot1, color = 'black', linewidth = 2.5, linestyle="-" , Label="psi=0")
    
            plt.legend(legende, loc = 'best')
            
            ax = plt.gca()
           
                
            ax.set_xlim(xmin, xmax)
            ax.set_ylim(ymin, ymax)
            ax.spines['left'].set_position(('data',xmin+1))
            ax.spines['bottom'].set_position(('data',0.))
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            plt.grid(linewidth=0.25)

            
            if printausnahme == False:
                plt.title(label=settext[j-1], loc="left", fontstyle='italic',fontsize=8,)
                #plt.text(xmin*0.96,0.035*ymax,settext[j-1],fontsize=8, color="black", bbox ={'facecolor':'white','alpha' : 0.7,'pad':3, "edgecolor" : "grey"}, zorder= 10)
        
            path = "Verifikation/"+name+ "/" +variabel+"/"+ resultat+"/"
            plt.savefig(path + name + "_" + resultat + "_" + zusatzname + "_"+ code +".png",dpi=300)
    
    
            plt.plot(x,plotcc1, color = 'black', linewidth = 2.5, linestyle="--" , Label="psi=1")

            if printausnahme == False:
                plt.plot(x,plotcc2, color = 'darkblue', linewidth = 1.5, linestyle="--" , Label="psi=1")           
            plt.plot(x,plotcc3, color = 'dodgerblue', linewidth = 1.5, linestyle="--" , Label="psi=1")         
            plt.plot(x,plotcc4, color = 'darkorange', linewidth = 1.5, linestyle="--" , Label="psi=1")
            if printausnahme == False:
                plt.plot(x,plotcc5, color = 'darkred', linewidth = 1.5, linestyle="--" , Label="psi=1")


            # schwarze linie
            plt.plot(x,plot1, color = 'black', linewidth = 2.5, linestyle="-" , Label="psi=0")
            plt.plot(x,plotcc1, color = 'black', linewidth = 2.5, linestyle="--" , Label="psi=1")
            
            printausnahme = False

            legende.append("Betonversagen")
            
 
            plt.legend(legende, loc = 'best')
            
            ax = plt.gca()
            ax.spines['left'].set_position(('data',xmin))
            ax.spines['bottom'].set_position(('data',0))
            ax.set_xlim([xmin, xmax])
            ax.set_ylim(ymin, ymax)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            

            
    
    

    
            plt.savefig(path + name + "_" + resultat + "_" + zusatzname + "_inkl CC" + "_"+ code + ".png",dpi=300)

            if legende[-1] == "Betonversagen":
                legende.remove("Betonversagen")
    
            plt.cla()
            plt.clf()
    
            print('\t'+ '\t'+ '\t' +"saved " + name + "_" + resultat)

            if setname[j-1] =="_tfv" and resultat == "as_z":
                break

    if variabel == "spezial":
        break

