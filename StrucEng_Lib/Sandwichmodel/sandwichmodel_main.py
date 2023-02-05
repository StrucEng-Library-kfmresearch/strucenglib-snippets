def Hauptfunktion(structure = "mdl", data = {}, step = "step_loads", Mindestbewehrung = True, Druckzoneniteration = True, Schubnachweis = 'vereinfacht',code = "sia", axes_scale = 100, plot_local_axes = True, plot_reinf = True):
    """
    Parameters
    ----------
    structure : obj
        Structure object.

    data : dict
        additionalproperties

    step : str
        step of calculation

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


    """


    import time
    import inputer
    import outputer
    import sandwichmodel_function as SM
    import statistics
    import rhino_functions as rf



    tic = time.time() #timer start
    
    print("\n**** sandwichmodel-analysis started... ****")
    #leeres Resultat dict.
    result_data = {str(step) : {"element" : {"as_xi_bot" : {}, "as_xi_top" : {}, "as_eta_bot" : {}, "as_eta_top" : {},"CC_bot" : {}, "CC_top" : {}, "Fall_bot" : {}, "Fall_top" : {}, "t_bot" : {}, "t_top" : {}, "k_bot" : {}, "k_top" : {},"psi_bot" : {}, "psi_top" : {}, "as_z" : {}, "m_shear_c" : {}, "m_cc_bot" : {}, "m_cc_top" : {}, "m_c_total" : {}, "xyz" : {}, "ex" : {}, "ey" : {}, "ez" : {}, "e_xi_bot" : {}, "e_xi_top" : {}, "e_eta_bot" : {}, "e_eta_top" : {}, }}}
    kmax = structure.element_count() # Anzahl Elemente, Startwert bei 1 nicht bei 0!
    
    k = 0    
    while k < kmax:
        # Input der Daten fuer Element k # inp = [i,mx,my,mxy,vx,vy,v0,nx,ny,nxy,h,d_strich_bot,d_strich_top,fc_k,theta_grad_kern,fs_d, alpha_bot, alpha_top, beta_bot, beta_top, Mindestbewehrung, Druckzoneniteration, Schubnachweis, xyz, ex,ey,ez]
        inp = inputer.inputer(structure,data,k,step, Mindestbewehrung, Druckzoneniteration, Schubnachweis, code)
        
        # Anwendung des Sandwichmodels auf Element k  # result_element = [i, as_xi, as_eta, as_z, fall, cc, t, k, psi, m_shear_c, m_cc, [xyz, ex, ey, ez, e_xi_bot, e_xi_top, e_eta_bot, e_eta_top], inp]
        result_element = SM.Sandwichmodel(inp)
        
        # Speichert Resultate von Sandwichmodel fuer Element k (result_element) im gesamt Resultatverzeichnis (result_data)
        result_data = outputer.outputer(result_data, result_element, step)
        
        # Plottet Achsen und Bewehrungsrichtungen auf Element k
        rf.plot_axes_BB(result_element, k, axes_scale, plot_local_axes, plot_reinf)
        

        k+=1
    
    toc = time.time()-tic #timer end
    print("\n**** sandwichmodel-analysis successful... duration: " +str(toc)+ "s ****" )
    

    tic = time.time() #timer start
    print("\n**** updating results... ****")

    # Speichert result_data in die structure.result dict von Compas FEA. damit die Compas FEA Funktion rhino.plot_data() genutzt werden kann
    structure.results[step]['element'].update(result_data[step]['element'])

    toc = time.time()-tic #timer end
    print("\n**** updating successful! duration: " +str(toc)+ "s **** ")
    return






def additionalproperty(data, prop_name = 'prop_name' , d_strich_bot = 40, d_strich_top = 40, fc_k = 30, theta_grad_kern = 45, fs_d=435, alpha_bot = 0, beta_bot = 90, alpha_top = 0, beta_top = 90):
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
        

