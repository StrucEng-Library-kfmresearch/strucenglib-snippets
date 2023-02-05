
import statistics
import mathematische_Hilfsfunktionen as mH

def inputer(structure, data, k, step, Mindestbewehrung, Druckzoneniteration, Schubnachweis, code):

   
    prop_name = structure.elements[k].element_property #name der property
    
    # SCHNITTKRAEFTE
    #sm1--> my
    sm1 = structure.results[step]['element']['sm1'][k].values()
    my = statistics.mean(list(sm1)) # Bildet den durchschnitt aller Integrationspunkte des Elements
    
    #sm2-->mx
    sm2 = structure.results[step]['element']['sm2'][k].values()
    mx = statistics.mean(list(sm2)) # Bildet den durchschnitt aller Integrationspunkte des Elements

    #sm3-->-mxy
    sm3 = structure.results[step]['element']['sm3'][k].values()
    mxy = -statistics.mean(list(sm3)) # Bildet den durchschnitt aller Integrationspunkte des Elements

    #sf1-->ny
    sf1 = structure.results[step]['element']['sf1'][k].values()
    ny = statistics.mean(list(sf1)) # Bildet den durchschnitt aller Integrationspunkte des Elements

    #sf2-->nx
    sf2 = structure.results[step]['element']['sf2'][k].values()
    nx = statistics.mean(list(sf2)) # Bildet den durchschnitt aller Integrationspunkte des Elements

    #sf3-->-nxy
    sf3 = structure.results[step]['element']['sf3'][k].values()
    nxy = -statistics.mean(list(sf3)) # Bildet den durchschnitt aller Integrationspunkte des Elements

    #sf4--> vy
    sf4 = structure.results[step]['element']['sf4'][k].values()
    vy = statistics.mean(list(sf4)) # Bildet den durchschnitt aller Integrationspunkte des Elements

    #sf5--> -vx
    sf5 = structure.results[step]['element']['sf5'][k].values()
    vx = -statistics.mean(list(sf5)) # Bildet den durchschnitt aller Integrationspunkte des Elements

    #vx+vy-->v0
    v0 = (vx**2+vy**2)**0.5

    #LOKALE KOORDINATEN (Achtung: diese Achsen werden von Abaqus anders eingelesen)
    # Nichtsdestotrotz ist es Wichtig dass diese Vektoren richtig definiert werden: Sie werden als lokale Achsen in Rhino geplottet und zu ihnen werden die Bewehrungsrichtungen definiert.
    # Unabhaengig wie die Z Achse ez hier definiert ist, ist die Z Achse in Abaqus immer die Normale zur Ebene, positiv ist nach Rechterhandregel der Daumen waehrend die Finger die Knotenpunkte in der Reihenfolge wie im INP abfahren. Im Rhino kann die "wahre" Z Achse ueber "Objektrichtung anzeigen" dargestellt und ueber "Richtung umkehren" geaendert werden...
    # Daher ist es wichtig, dass ez gleich definiert wird wie die Objektrichtung in Rhino. Dies muss manuell erfolgen!
    ex = structure.elements[k].axes['ex'] #
    ey = structure.elements[k].axes['ey'] # diese Achse wird die lokale X koordinate in Abaqus (projeziert auf die Meshoberflaeche). Beim Einlesen der Schnittkraefte wird dies beruecksichtigt.
    ez = structure.elements[k].axes['ez'] # 

    # Element centroid
    xyz= structure.element_centroid(element=k)

    


    # Dicke des Elements aus der Section von COMPAS FEA
    sec_name = structure.element_properties[prop_name].section
    h = structure.sections[sec_name].geometry['t']
    

    # Daten aus den Zusaetlichen Parametern (Additionalproperty) (d_strich_bot,d_strich_top,fc_k,theta_grad_kern,fs_d, alpha_bot, alpha_top, beta_bot, beta_top)
    d_strich_bot = data[prop_name]['d_strich_bot']
    d_strich_top = data[prop_name]['d_strich_top']
    fc_k = data[prop_name]['fc_k']
    theta_grad_kern = data[prop_name]['theta_grad_kern']
    fs_d = data[prop_name]['fs_d']
    alpha_bot = data[prop_name]['alpha_bot']
    alpha_top = data[prop_name]['alpha_top']
    beta_bot = data[prop_name]['beta_bot']
    beta_top = data[prop_name]['beta_top']



    
    

    inp = [k,mx,my,mxy,vx,vy,v0,nx,ny,nxy,h,d_strich_bot,d_strich_top,fc_k,theta_grad_kern,fs_d, alpha_bot, alpha_top, beta_bot, beta_top, Mindestbewehrung, Druckzoneniteration, Schubnachweis, code, xyz, ex, ey, ez,]
    return inp






