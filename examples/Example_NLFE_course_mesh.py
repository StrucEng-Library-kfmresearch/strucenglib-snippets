
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Example_with_all_functionalities
# Author: Marius Weber (ETHZ, HSLU T&A)
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


# Import packages
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
from compas_fea.cad import rhino
from compas_fea.structure import ElasticIsotropic
from compas_fea.structure import MPCStiff
from compas_fea.structure import CMMUsermat
from compas_fea.structure import ElementProperties as Properties
from compas_fea.structure import GeneralStep
from compas_fea.structure import GravityLoad
from compas_fea.structure import AreaLoad
from compas_fea.structure import PointLoad
from compas_fea.structure import GeneralDisplacement
from compas_fea.structure import FixedDisplacement
from compas_fea.structure import FixedDisplacementXX
from compas_fea.structure import FixedDisplacementYY
from compas_fea.structure import FixedDisplacementZZ
from compas_fea.structure import PinnedDisplacement
from compas_fea.structure import RollerDisplacementX
from compas_fea.structure import RollerDisplacementZ
from compas_fea.structure import RollerDisplacementXY
from compas_fea.structure import RollerDisplacementYZ
from compas_fea.structure import RollerDisplacementXZ
from compas_fea.structure import ShellSection
from compas_fea.structure import MPCSection
from compas_fea.structure import Structure

from strucenglib.prepost_functions import calc_loc_coor
from strucenglib.prepost_functions import plot_loc_axes
from strucenglib.prepost_functions import plot_nr_elem
from strucenglib.prepost_functions import plot_nr_nodes
from strucenglib.prepost_functions import area_load_generator_elements
from strucenglib.prepost_functions import Normalspurbahnverkehr_load_generator
from strucenglib.prepost_functions import verification
from strucenglib.sandwichmodel import sandwichmodel_main as SMM


# Geoemtrie/Sections/Materials/Properties/Constraints 
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Initialisieren
name = 'NLFE'
path = 'C:\Temp\\'
mdl = Structure(name=name, path=path)

# Structure
mdl = Structure(name=name, path=path)

# Shell Elements
rhino.add_nodes_elements_from_layers(mdl, mesh_type='ShellElement', layers=[ 'elset_deck' ] ) 


# Sets for constraints
rhino.add_sets_from_layers(mdl, layers=[ 'nset_pinned' ] )

# Nonlinear Materials
geo={'R_Rohr':-1, 'rho':0.0000025, 'oo':30, 'uu':30}
concrete={'beton':2, 'fcc':50, 'vc':0, 'ecu':-0.002, 'k_E':10000, 'theta_b0':2, 'theta_b1':1, 'k_riss':0, 'Entfestigung':0, 'lambdaTS':0.67, 'srmx':1, 'srmy':1, 'Begrenzung':2, 'KritQ':0, 'winkelD':45, 'k_vr':1, 'fswy':500}
reinf_1L={'stahl':1,'zm':2,'fsy':500,'fsu':600,'esu':0.8,'esv':0.02,'Es':200000,'ka':-1,'kb':-1,'kc':-1,'as':1,'dm':20,'psi':-90}
reinf_2L={'stahl':1,'zm':2,'fsy':600,'fsu':700,'esu':0.8,'esv':0.02,'Es':200000,'ka':-1,'kb':-1,'kc':-1,'as':1,'dm':20,'psi':0}
reinf_3L={'stahl':1,'zm':2,'fsy':700,'fsu':800,'esu':0.8,'esv':0.02,'Es':200000,'ka':-1,'kb':-1,'kc':-1,'as':1,'dm':20,'psi':0}
reinf_4L={'stahl':1,'zm':2,'fsy':800,'fsu':900,'esu':0.8,'esv':0.02,'Es':200000,'ka':-1,'kb':-1,'kc':-1,'as':1,'dm':20,'psi':-90}

mdl.add(CMMUsermat(name='elset_deck_element_mat', geo=geo, concrete=concrete, reinf_1L=reinf_1L, reinf_2L=reinf_2L, reinf_3L=reinf_3L, reinf_4L=reinf_4L,)) 

# Shell Sections, Properties, additional Properties, set local coordiantes (The local z-axed is adjusted by using "object direction" in Rino) 

semi_loc_coords=calc_loc_coor(layer='elset_deck', PORIG=[0,0,0],PXAXS=[1,0,0]) # use Rhino command EvaluatePt to get the world x,y,z coor for PORIG
mdl.add(ShellSection(name='elset_deck_element_sec', t=400, semi_loc_coords=semi_loc_coords, nn=40, offset_mode='mid'))
mdl.add(Properties(name='elset_deck_element_prop', material='elset_deck_element_mat', section='elset_deck_element_sec', elset='elset_deck'))


# Grafical plots 
plot_loc_axes(mdl, axes_scale=50) # Plot Local coordinates 
plot_nr_elem(mdl) # Plot Element Numbers
plot_nr_nodes(mdl)  # Plot Node Numbers

# Constrains (Displacements)
mdl.add([GeneralDisplacement(name='nset_pinned_set_disp',  x=0, y=0, z=0, xx=0, yy=0, zz=0, nodes='nset_pinned'),])


# Loads and steps
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Gravity Loads
mdl.add(GravityLoad(name='load_gravity',  x=0.0,  y=0.0,  z=1.0, elements=[ 'elset_deck' ] ))

# Area Load
loaded_element_numbers=area_load_generator_elements(mdl,layer='area_load_left') 
mdl.add(AreaLoad(name='area_load_left', elements=loaded_element_numbers,x=0,y=0,z=0.2)) 
 

# Steps
mdl.add([
GeneralStep(name='step_1',   displacements=[ 'nset_pinned_set_disp' ] ,  nlgeom=False),
GeneralStep(name='step_2',  loads=['load_gravity'] ,   nlgeom=False, increments=1),
GeneralStep(name='step_3',  loads=['area_load_left'] ,   nlgeom=False, increments=1),
])
mdl.steps_order = [ 'step_1', 'step_2', 'step_3' ] 


# Run analyses
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
#mdl.analyse_and_extract(software='ansys_sel', fields=[ 'u', 'sf', 's', 'eps', 'sig_sr'], lstep = ['step_3'], ansys_version='22') 
mdl.analyse_and_extract(software='ansys_sel', fields=[ 'u', 'sf'], lstep = ['step_3'], ansys_version='22') 




# Plot Results
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Plot Results for step_3
#rhino.plot_data(mdl, lstep='step_3', field='uz', scale=10, cbar_size=1, source='CMMUsermat') # Ploten der Verformungen uz (Resultate: Knoten)
#rhino.plot_data(mdl, lstep='step_3', field='ux', cbar_size=1, source='CMMUsermat') # Ploten der Verformungen ux (Resultate: Knoten)
#rhino.plot_data(mdl, lstep='step_3', field='uy', cbar_size=1, source='CMMUsermat') # Ploten der Verformungen uy (Resultate: Knoten)
#rhino.plot_data(mdl, lstep='step_3', field='sf1', cbar_size=1, source='CMMUsermat') # Ploten der verallgemeinerten Spannungen (Resultate: Elementmitte)
#rhino.plot_data(mdl, lstep='step_3', field='sf2', cbar_size=1, source='CMMUsermat') # Ploten der verallgemeinerten Spannungen (Resultate: Elementmitte)
#rhino.plot_data(mdl, lstep='step_3', field='sf3', cbar_size=1, source='CMMUsermat') # Ploten der verallgemeinerten Spannungen (Resultate: Elementmitte)
#rhino.plot_data(mdl, lstep='step_3', field='sf4', cbar_size=1, source='CMMUsermat') # Ploten der verallgemeinerten Spannungen (Resultate: Elementmitte)
#rhino.plot_data(mdl, lstep='step_3', field='sf5', cbar_size=1, source='CMMUsermat') # Ploten der verallgemeinerten Spannungen (Resultate: Elementmitte)
#rhino.plot_data(mdl, lstep='step_3', field='sm1', cbar_size=1, source='CMMUsermat') # Ploten der verallgemeinerten Spannungen (Resultate: Elementmitte)
#rhino.plot_data(mdl, lstep='step_3', field='sm2', cbar_size=1, source='CMMUsermat') # Ploten der verallgemeinerten Spannungen (Resultate: Elementmitte)
#rhino.plot_data(mdl, lstep='step_3', field='sm3', cbar_size=1, source='CMMUsermat') # Ploten der verallgemeinerten Spannungen (Resultate: Elementmitte)
#rhino.plot_principal_stresses(mdl, step='step_3', shell_layer='top', cbar_size=0.5, scale=10**1, numeric='no', values='3') # Hauptspannungen 3 top (Resultate: Gauspunkte)
#rhino.plot_principal_stresses(mdl, step='step_3', shell_layer='top', cbar_size=0.5, scale=1000, numeric='no', values='1') # Hauptspannungen 1 top (Resultate: Gauspunkte)
#rhino.plot_principal_stresses(mdl, step='step_3', shell_layer='bot', cbar_size=0.5, scale=10**1, numeric='no', values='3') # Hauptspannungen 3 bot (Resultate: Gauspunkte)
#rhino.plot_principal_stresses(mdl, step='step_3', shell_layer='bot', cbar_size=0.5, scale=10**1, numeric='no', values='1') # Hauptspannungen 1 bot (Resultate: Gauspunkte)
#rhino.plot_principal_strains(mdl, step='step_3', shell_layer='top', cbar_size=0.5, scale=10**5, numeric='no', values='3') # Hauptverzerrungen 3 top (Resultate: Gauspunkte)
#rhino.plot_principal_strains(mdl, step='step_3', shell_layer='top', cbar_size=0.5, scale=10**5, numeric='no', values='1') # Hauptverzerrungen 1 top (Resultate: Gauspunkte)
#rhino.plot_principal_strains(mdl, step='step_3', shell_layer='bot', cbar_size=0.5, scale=10**5, numeric='no', values='3') # Hauptverzerrungen 3 bot (Resultate: Gauspunkte)
#rhino.plot_principal_strains(mdl, step='step_3', shell_layer='bot', cbar_size=0.5, scale=10**5, numeric='no', values='1') # Hauptverzerrungen 1 bot (Resultate: Gauspunkte)
#rhino.plot_steel_stresses(mdl, step='step_3', Reinf_layer='RL_1', cbar_size=0.5, scale=1.3, numeric='no') # Stahlspannungen am Riss 1. Bewehrungslage (Resultate: Gauspunkte)
#rhino.plot_steel_stresses(mdl, step='step_3', Reinf_layer='RL_2', cbar_size=0.5, scale=1.3, numeric='no') # Stahlspannungen am Riss 2. Bewehrungslage (Resultate: Gauspunkte)
#rhino.plot_steel_stresses(mdl, step='step_3', Reinf_layer='RL_3', cbar_size=0.5, scale=1.3, numeric='no') # Stahlspannungen am Riss 3. Bewehrungslage (Resultate: Gauspunkte)
#rhino.plot_steel_stresses(mdl, step='step_3', Reinf_layer='RL_4', cbar_size=0.5, scale=1.3, numeric='no') # Stahlspannungen am Riss 4. Bewehrungslage (Resultate: Gauspunkte)
rhino.plot_principal_shear(mdl, step='step_3', field='sm1', cbar_size=0.5, scale=4, numeric='no') # Hauptverzerrungen 1 bot (Resultate: Gauspunkte)
