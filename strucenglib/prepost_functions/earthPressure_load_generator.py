 # Author(s): Sophia Kuhn (ETHZ)

import os 
import math as m
import rhinoscriptsyntax as rs
import scriptcontext
import System.Guid, System.Drawing.Color
from compas_fea.structure import Structure
from compas_fea.cad import rhino
from compas_fea.structure import AreaLoad
from strucenglib.prepost_functions import area_load_generator_elements



def earthPressure_gravel_generator(structure, elements,h_G, gamma_E, phi_k, gamma_G=1, verbalise=True):

    '''
    This function calculates the earth pressure area load magnitude that results from the layers of soil that lie above the slab deck.
    And then this function adds this caluclated load value as a load to the structure object.

    Parameters
    ----------
    structure: structureObject
        the object representing the structure to be analysed
    elements: List[str]
        List of the names of the layers, which contain the elements that should be loaded   
    h_G : float
        Gravel layer hight [mm]
    gamma_E : float
        sp. Weight [N/mm3] (e.g. Verdichteter Schotter 0.000020 N/mm3 )
    phi_k: int
        ..[Degree] (e.g. 30)
    verbalise: bool
        Defining weather to verbalise the calculation 


    Returns
    ----------
    List[str]
        List of load names, which were generated within this function: ['earthPressure_backfill']

    Limitations
    -------------
    - NO waterpressure is considered (for low water levels), 
    - constant gamma_E is considered (for gravel and backfill), so no layerd ground
    '''


    #calc. Ko
    Ko = 1 - m.sin(m.radians(phi_k))

    # calc eath pressure at slab deck surface (resulting from gravel layer)
    p = gamma_G*(Ko * gamma_E * h_G) #[N/mm2]  (gamma_E: [N/mm3])

    # verbalise
    if verbalise:
        print('The earth pressure resulting from the gravel layer is calculated to be: ', p, ' N/mm2 ;',p*1000, ' kN/m2'  )

    #add load to structur object
    structure.add(AreaLoad(name='earthPressure_gravel', elements=elements, x=0,y=0,z=p, axes ='global')) #postive z direction means downwards here 

    #return the name of the load that was saved to the structure object
    return ['earthPressure_gravel']






def earthPressure_backfill_generator(structure, elements, h_w, t_p, h_G, gamma_E, phi_k, gamma_G=1, verbalise=True):
    
    '''
    This function calculates the earth pressure area load magnitude that results from the backfill and generates the correspondin area load.

    Parameters
    ----------
    structure: structureObject
        the object representing the structure to be analysed
    elements: List[str]
        List of the names of the layers, which contain the elements that should be loaded   
    h_w : float
        Wall hight [mm]
    t_p : float
        Deck Slab Thickness [mm]
    h_G : float
        Gravel layer hight [mm]
    gamma_E : float
        sp. Weight [N/mm3] (e.g. Verdichteter Schotter 0.000020 N/mm3 )
    phi_k: int
        ..[Degree] (e.g. 30)
    verbalise: bool
        Defining weather to verbalise the calculation 


    Returns
    ----------
    List[str]
        List of load names, which were generated within this function: ['earthPressure_backfill']

    Limitations
    -------------
    - NO waterpressure is considered (for low water levels), 
    - constant gamma is considered (for gravel and backfill), so no layerd ground
    '''
    

    # Basic definitions
    #-------------------------------------------------------

    #calc. Ko
    Ko = 1 - m.sin(m.radians(phi_k)) 

    # calculate hight over which the earth pressure is active onto the structure
    # (only correct for with offsetmodelling and with MPCs and voute)
    h_ep = h_w  + t_p #[mm]

    # celculate earth pressure
    # at top of slab deck (for the sqare of the earth pressure)
    p_t = Ko * gamma_E * h_G #[N/mm2]

    # at foundation hight (for the triangle of the force pressure)
    p_f = Ko * gamma_E * h_ep #[N/mm2] 


    # calculate resulting force  (area of earth pressure)
    R_sqare=gamma_G* p_t * h_ep  #[N/mm] 
    R_triangle = gamma_G*1/2 *p_f * h_ep #[N/mm] 
    R_tot=R_sqare+R_triangle #[N/mm] 


    # dirtribute uniformily on whole elset hight
    q_ep_r=R_tot/ h_w  #[N/mm2]

    # verbalise
    if verbalise:
        print('The earth pressure resulting from the backfill is calculated to be: ', q_ep_r, ' N/mm2 ;',q_ep_r*1000, ' kN/m2' )

    structure.add(AreaLoad(name='earthPressure_backfill', elements=elements, x=0,y=0,z=q_ep_r, axes ='local')) # postive z-dir is inwards here

    # return q_er_r 
    return ['earthPressure_backfill']


def earthPressure_liveload_generator(structure, s, beta, L, h_w, t_p, phi_k,gamma_Q=1, direction='positive', name=None, verbalise=True):
    
    '''
    This function calculates the earth pressure area load magnitude that results from the live load of a track
    and generates the correspondin area load.

    Parameters
    ----------
    structure: structureObject
        object representing the structure to be analysed
    s : float
        Distance between origin and middle axis of the track 
    h_w : float
        Wall hight [mm]
    beta : float
        Angle between global y-axis and track axis [Degree], should be in range[-90,90]
    L : float
        Span of the frame bridge [mm]
    t_p : float
        Deck Slab Thickness [mm]
    phi_k: int
        ..[Degree] (e.g. 30)
    direction: str
        Direction in which the earthPressure should act (also decids on which wall it is applied) (e.g. 'positive')
    name : str
        Name of the track (e.g. "Track1")
    verbalise: bool
        Defining weather to verbalise the calculation 


    Returns
    ----------
    List[str]
        List of load names, which were generated within this function

    Limitations/Specification
    -------------
    - So far the earth pressure live load is only applied to one side (at x=0), so far this function is not able to apply earth pressure on both wall sides
    - Has to be used after the the Normalspurbahnverkehr_load_generator function was executed (as this function uses the created Mittelachse)
    '''

    # Calculate magnitude 
    #-------------------------------------------------------
    # calculate magnitude of area load
    q = 0.052 #[N/mm2] = 52[kN/m2] From PAIngB B1.3 Page 72 (SBB specific norm)
    # z = 700 [mm] #From PAIngB B1.3 Page 72
    #TODO checken ob das so richtig ist mit dem If sentence (vgl bericht Hero), need z?
    # if h_g > z:
    #     z=h_g
    Ko = 1-m.sin(m.radians(phi_k))
    p = gamma_Q*(Ko * q) #[N/mm2]


    #Initialize
    load_name_list=[]

    #Case 1: apply earth pressure in positive y direction (wall 2)
    if direction in  [ 'positive', 'all', 'both']:
            # Create layer
        #-------------------------------------------------------
        # define layer name ( and later name of area load)
        if name == None:
            layer_name = "EarthPressure_liveLoad_area_pos"
        else:
            layer_name = "{}_EarthPressure_liveLoad_area_pos".format(name)



        # create the new layer
        if rs.IsLayer(layer_name):
            rs.PurgeLayer(layer_name)
            scriptcontext.doc.Layers.Add(layer_name, System.Drawing.Color.Green)
        else:
            scriptcontext.doc.Layers.Add(layer_name, System.Drawing.Color.Green)
        
        # set layer to current active layer
        rs.CurrentLayer(layer_name)

        # Generate polyline of area load
        #-------------------------------------------------------
        # Startpunkt der Mittelachse (Annahme: Globaler Nullpunkt immer bei x=0,y=0,z=0)
        point_start_x=s
        point_start_y=0

        #calculation of corner point coordinates in wall 1
        # y is always 0
        ep_width=3800 #[mm] # From PAIngB B1.3 Page 72 (SBB specific norm)
        x_A= point_start_x +ep_width/2
        z_A = -t_p
        x_B= point_start_x +ep_width/2
        z_B = -h_w-t_p
        x_C= point_start_x -ep_width/2
        z_C = -h_w-t_p
        x_D= point_start_x -ep_width/2
        z_D = -t_p

        # creation of polyline, and add to active layer
        rs.AddPolyline([(x_A,0,z_A),(x_B,0,z_B),(x_C,0,z_C),(x_D,0,z_D), (x_A,0,z_A)])



        # Add area load to loaded elements
        #-------------------------------------------------------
        # determine which elements are loaded
        loaded_element_numbers=area_load_generator_elements(structure, layer_name)
        print('pos: ',loaded_element_numbers)

        #define load name
        if name == None:
            load_name='earthPressure_liveLoad_pos'
        else:
            load_name='earthPressure_liveLoad_pos_{}'.format(name)

        load_name_list.append(load_name) #save load name to be returned

        # add load
        structure.add(AreaLoad(load_name, elements=loaded_element_numbers,x=0,y=0,z=p,axes ='local')) # postive z-dir is inwards here


    #Case 2: apply earth pressure in positive y direction (wall 2)
    if direction in  [ 'negative', 'all', 'both']:
            # Create layer
        #-------------------------------------------------------
        # define layer name ( and later name of area load)
        if name == None:
            layer_name = "EarthPressure_liveLoad_area_neg"
        else:
            layer_name = "{}_EarthPressure_liveLoad_area_neg".format(name)


        # create the new layer
        if rs.IsLayer(layer_name):
            rs.PurgeLayer(layer_name)
            scriptcontext.doc.Layers.Add(layer_name, System.Drawing.Color.Green)
        else:
            scriptcontext.doc.Layers.Add(layer_name, System.Drawing.Color.Green)
        
        # set layer to current active layer
        rs.CurrentLayer(layer_name)

        # Generate polyline of area load
        #-------------------------------------------------------
        # Startpunkt der Mittelachse auf wall 1 (Annahme: Globaler Nullpunkt immer bei x=0,y=0,z=0)
        point_start_x=s
        # Endpoint der Mittelchse on wall 2
        point_start_x_w2 = point_start_x + m.tan(m.radians(beta))*L


        #calculation of corner point coordinates in wall 2
        ep_width=3800 #[mm] # From PAIngB B1.3 Page 72 (SBB specific norm)
        x_A= point_start_x_w2 +ep_width/2
        z_A = -t_p
        x_B= point_start_x_w2 +ep_width/2
        z_B = -h_w-t_p
        x_C= point_start_x_w2 -ep_width/2
        z_C = -h_w-t_p
        x_D= point_start_x_w2 -ep_width/2
        z_D = -t_p

        rs.AddPolyline([(x_A,L,z_A),(x_B,L,z_B),(x_C,L,z_C),(x_D,L,z_D), (x_A,L,z_A)])
    

        # Add area load to loaded elements
        #-------------------------------------------------------
        
        # determine which elements are loaded
        loaded_element_numbers=area_load_generator_elements(structure, layer_name)
        print('neg: ',loaded_element_numbers)
        
        #define load name
        if name == None:
            load_name='earthPressure_liveLoad_neg'
        else:
            load_name='earthPressure_liveLoad_neg_{}'.format(name)

        load_name_list.append(load_name) #save load name to be returned

        # add load
        structure.add(AreaLoad(load_name, elements=loaded_element_numbers,x=0,y=0,z=p,axes ='local')) # postive z-dir is inwards here


    # Case C: invalid input for direction
    if direction not in  ['positive', 'negative', 'all', 'both']:
        raise ValueError('The direction defined is not valid. Please choose between "postive", "negative, or "all".')





    # set default layer back to active layer
    rs.CurrentLayer('Default')

    # verbalise
    if verbalise:
        print('The earth pressure resulting from the live load is calculated to be: ', p, ' N/mm2 ;',p*1000, ' kN/m2'  )

    #return of name of generated area load(s) as a list
    return load_name_list


