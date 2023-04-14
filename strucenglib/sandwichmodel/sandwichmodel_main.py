def Hauptfunktion(structure = "mdl", data = {}, lstep = None, Mindestbewehrung = True, Druckzoneniteration = True, Schubnachweis = 'vereinfacht',code = "sia", axes_scale = 100, plot_local_axes = True, plot_reinf = True):
    """
    Parameters
    ----------
    structure : obj
        Structure object.

    data : dict
        additionalproperties

    lstep : str
        step (time) of calculation

    Mindestbewehrung : bool
        Mindestbewehrung beruecksichtigen?

    Druckzoneniteration : bool
        Druckzonenhoehe iterieren?

    Schubnachweis : str
        definiert ob der Schubnachweis nach sia ('sia') oder dem vereinfachten verfahren ('vereinfacht') gefuehrt werden soll.

    code : str
        Normfunktionen nach SIA ('sia') oder Eurocode ('EC')

    axes_scale : float
        scalefactor for all axes

    plot_local_axes : bool
        lokale Achsen auf jedes Element plotten?

    plot_reinf : bool
        Bewehrungsrichtungen auf jedes Element plotten?

    beta: float
        Definiert Erhoehungsfaktor der Lasten gegenueber dem Basis-Lastfall.  

    """


    import time
    import inputer
    import outputer
    import sandwichmodel_function as SM
    import statistics
    import rhino_functions as rf




    
    print('')
    print('')
    print('Run sandwichmodel analysis')
    print('--------------------------------------------------------')
    print('Sandwichmodel analysis is running ... please wait ... ' )
    tic = time.time() #timer start
    kmax = structure.element_count() # Anzahl Elemente, Startwert bei 1 nicht bei 0!
       
    
   
    
    for single_lstep in lstep:
        k = 0 
        step=single_lstep

        #leeres Resultat dict.
        result_data = {str(step) : {"element" : {"as_xi_bot" : {}, "as_xi_top" : {}, "as_eta_bot" : {}, "as_eta_top" : {},"CC_bot" : {}, "CC_top" : {}, "Fall_bot" : {}, "Fall_top" : {}, "t_bot" : {}, "t_top" : {}, "k_bot" : {}, "k_top" : {},"psi_bot" : {}, "psi_top" : {}, "as_z" : {}, "m_shear_c" : {}, "m_cc_bot" : {}, "m_cc_top" : {}, "m_c_total" : {}, "xyz" : {}, "ex" : {}, "ey" : {}, "ez" : {}, "e_xi_bot" : {}, "e_xi_top" : {}, "e_eta_bot" : {}, "e_eta_top" : {}, }}}
        

        # Element bzw. Element set fur Nachweisschnitt V bestimmen
        #k_NS_V=structure.sets['NS_Schnitt_V']
        
        while k < kmax:
            # Berechnung SM nur fuer Shell Elemente (d.h. ele_type=1 -> Shell; ele_type=0 -> MPC oder andere Elemente)
            ele_type = structure.results[step]['element']['ele_type'][k].values()

            if ele_type[0] == 1.0:            
            
                # Input der Daten fuer Element k # inp = [i,mx,my,mxy,vx,vy,v0,nx,ny,nxy,h,d_strich_bot,d_strich_top,fc_k,theta_grad_kern,fs_d, alpha_bot, alpha_top, beta_bot, beta_top, Mindestbewehrung, Druckzoneniteration, Schubnachweis, xyz, ex,ey,ez]
                inp = inputer.inputer(structure,data,k,step, Mindestbewehrung, Druckzoneniteration, Schubnachweis, code)

                # Anwendung des Sandwichmodels auf Element k  # result_element = [i, as_xi, as_eta, as_z, fall, cc, t, k, psi, m_shear_c, m_cc, [xyz, ex, ey, ez, e_xi_bot, e_xi_top, e_eta_bot, e_eta_top], inp]
                result_element = SM.Sandwichmodel(inp) #,k_NS_V)
                
                # Speichert Resultate von Sandwichmodel fuer Element k (result_element) im gesamt Resultatverzeichnis (result_data)
                result_data = outputer.outputer(result_data, result_element, step, ele_type, k)
                
                # Plottet Achsen und Bewehrungsrichtungen auf Element k TODO: PLOT IN PREPROCESSING NEHMEN
                # rf.plot_axes_BB(result_element, k, axes_scale, plot_local_axes, plot_reinf)
            else:
                # Speichert Resultate von Sandwichmodel fuer nicht Shell elemente
                result_data = outputer.outputer(result_data, result_element, step, ele_type, k)

            k+=1
        
        # Speichert result_data in die structure.result dict von Compas FEA. damit die Compas FEA Funktion rhino.plot_data() genutzt werden kann
        print(step)
        structure.results[step]['element'].update(result_data[step]['element'])

    toc = time.time()-tic #timer end
    print('Sandwichmodel analysis successfull finished in {0:.3f} s'.format(toc))

    return




def additionalproperty(data, prop_name = 'prop_name' , d_strich_bot = 40, d_strich_top = 40, fc_k = 30, theta_grad_kern = 45, fs_d=435, alpha_bot = 0, beta_bot = 90, alpha_top = 0, beta_top = 90, ex=None, ey=None, ez=None):
    """
    Parameters
    ----------
            
    data : dict
        additionalproperties

    prop_name : str
        name of compas_fea ElementProperties object for which the following additional properties are 

    d_strich_bot : int
        Distanz zwischen Unterkante Element und Schwerpunkt beider unteren Bewehrungslagen in mm

    d_strich_top : int
        Distanz zwischen Oberkante Element und Schwerpunkt beider oberen Bewehrungslagen in mm

    fc_k : int
        Zylinderdruckfestigkeit Beton charakteristisch in N/mm2

    theta_grad_kern : int
        Neigung Druckfeld im Kern SIA & EC in Grad

    alpha_bot : int
        Neigung der ersten unteren Deckelbewehrung zur lokalen x-achse in Grad, positiv gegen y-Achse

    alpha_top : int
        Neigung der ersten oberen Deckelbewehrung zur lokalen x-achse in Grad, positiv gegen y-Achse

    beta_bot : int
        Neigung der zweiten unteren Deckelbewehrung zur lokalen x-achse in Grad, positiv gegen y-Achse

    beta_top : int
        Neigung der zweiten oberen Deckelbewehrung zur lokalen x-achse in Grad, positiv gegen y-Achse

    ex : int
        Einheitsvektor der lokalen x Koordinate

    ey : int
        Einheitsvektor der lokalen y Koordinate

    ez : int
        Einheitsvektor der lokalen z Koordinate        
    """


    #d_strich_bot,d_strich_top,fc_k,theta_grad_kern,fs_d, alpha_bot, alpha_top, beta_bot, beta_top
    data.update({prop_name : {}})
    data[prop_name].update({'d_strich_bot' : d_strich_bot})
    data[prop_name].update({'d_strich_top' : d_strich_top})
    data[prop_name].update({'fc_k' : fc_k})
    data[prop_name].update({'theta_grad_kern' : theta_grad_kern})
    data[prop_name].update({'fs_d' : fs_d})
    data[prop_name].update({'alpha_bot' : alpha_bot})
    data[prop_name].update({'alpha_top' : alpha_top})
    data[prop_name].update({'beta_bot' : beta_bot})
    data[prop_name].update({'beta_top' : beta_top})
    data[prop_name].update({'ex' : ex})
    data[prop_name].update({'ey' : ey})
    data[prop_name].update({'ez' : ez})
    return data


def max_values(structure, step): #Diese Funktion gibt lediglich die maximalen Bewehrungsgehaelter als print aus
    """
    Parameters
    ----------
    structure : obj
        Structure object.

    step : str
        step of calculation
    """


    list = ['as_xi_bot', 'as_xi_top', 'as_eta_bot', 'as_eta_top']
    for value in list:
        val = structure.results[step]['element'][value]
        max_value = max(val.values())
        max_key = max(val, key=val.get)
        xyz = structure.results[step]['element']['xyz'][max_key]

        print(value + "_max: " + str(max_value.values()) + " mm2/m @ [x,y,z] = " + str(xyz))
        

