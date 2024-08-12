
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
#from compas_fea.structure import RollerDispslacementY
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
rhino.add_nodes_elements_from_layers(mdl, mesh_type='ShellElement', layers=[ 'elset_deck', 'elset_right', 'elset_left'] ) 

# MPC Elements
rhino.add_nodes_elements_from_layers(mdl, line_type='MPCElement', layers='elset_mpc')

# Sets for constraints
rhino.add_sets_from_layers(mdl, layers=[ 'nset_pinned' ] )

# Linear elastic Materials

# Shell Materials
mdl.add(ElasticIsotropic(name='elset_deck_element_mat', E=35000, v=0.0, p=2500/10**9)) 
mdl.add(ElasticIsotropic(name='elset_right_element_mat', E=35000, v=0.0, p=2500/10**9))
mdl.add(ElasticIsotropic(name='elset_left_element_mat', E=35000, v=0.0, p= 2500/10**9))

# MPC Materials
mdl.add(MPCStiff(name='elset_mpc_element_mat'))

# Shell Sections, Properties, additional Properties, set local coordiantes (The local z-axed is adjusted by using "object direction" in Rino) 
data = {}
semi_loc_coords=calc_loc_coor(layer='elset_deck', PORIG=[0,0,2980],PXAXS=[1,0,0])
mdl.add(ShellSection(name='elset_deck_element_sec', t=400, semi_loc_coords=semi_loc_coords, nn=40))
mdl.add(Properties(name='elset_deck_element_prop', material='elset_deck_element_mat', section='elset_deck_element_sec', elset='elset_deck'))
SMM.additionalproperty(data, prop_name='elset_deck_element_prop', d_strich_bot = 40, d_strich_top = 40, fc_k = 50, theta_grad_kern = 45, fs_d = 600, alpha_bot = 0, beta_bot = 90, alpha_top = 0, beta_top = 90, ex=semi_loc_coords[4], ey=semi_loc_coords[5], ez=semi_loc_coords[6])

semi_loc_coords=calc_loc_coor(layer='elset_right', PORIG=[0,5400,0],PXAXS=[1,0,0]) 
mdl.add(ShellSection(name='elset_right_element_sec', t=400, semi_loc_coords=semi_loc_coords, nn=40))
mdl.add(Properties(name='elset_right_element_prop', material='elset_right_element_mat', section='elset_right_element_sec', elset='elset_right'))
SMM.additionalproperty(data, prop_name='elset_right_element_prop', d_strich_bot = 40, d_strich_top = 40, fc_k = 50, theta_grad_kern = 45, fs_d = 600, alpha_bot = 0, beta_bot = 90, alpha_top = 0, beta_top = 90, ex=semi_loc_coords[4], ey=semi_loc_coords[5], ez=semi_loc_coords[6])
 
semi_loc_coords=calc_loc_coor(layer='elset_left', PORIG=[0,0,0],PXAXS=[1,0,0])  
mdl.add(ShellSection(name='elset_left_element_sec', t=400, semi_loc_coords=semi_loc_coords, nn=40))
mdl.add(Properties(name='elset_left_element_prop', material='elset_left_element_mat', section='elset_left_element_sec', elset='elset_left'))
SMM.additionalproperty(data, prop_name='elset_left_element_prop', d_strich_bot = 40, d_strich_top = 40, fc_k = 50, theta_grad_kern = 45, fs_d = 600, alpha_bot = 0, beta_bot = 90, alpha_top = 0, beta_top = 90, ex=semi_loc_coords[4], ey=semi_loc_coords[5], ez=semi_loc_coords[6])

# MPC Sections
mdl.add(MPCSection(name='sec_mpc'))
mdl.add(Properties(name='elset_mpc_element_prop', material='elset_mpc_element_mat', section='sec_mpc', elset='elset_mpc'))

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
mdl.add(AreaLoad(name='area_load_left', elements=loaded_element_numbers,x=0,y=0,z=0.001)) 

# Area Load 2
loaded_element_numbers=area_load_generator_elements(mdl,layer='area_load_right') 
mdl.add(AreaLoad(name='area_load_right', elements=loaded_element_numbers,x=0,y=0,z=0.001)) 

# Normalspurverkehr Load generator 
return_values_Gleis=Normalspurbahnverkehr_load_generator(mdl,name='Gleis', l_Pl=5400, h_Pl=400, s=5000, beta=-30, q_Gl=4.8, b_Bs=2500, h_Strich=300, Q_k=225*1000, y_A=5000)


# Steps
mdl.add([
GeneralStep(name='step_1',   displacements=[ 'nset_pinned_set_disp' ] ,  nlgeom=False),
GeneralStep(name='step_2',  loads=['load_gravity'] ,   nlgeom=False, increments=1),
GeneralStep(name='step_3',  loads=['area_load_left', 'area_load_right'] ,   nlgeom=False, increments=1),
GeneralStep(name='step_4',  loads=return_values_Gleis ,   nlgeom=False),
])
mdl.steps_order = [ 'step_1', 'step_2', 'step_3' , 'step_4'  ] 


# Run analyses
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
mdl.analyse_and_extract(software='ansys_sel', fields=[ 'u', 'sf'], lstep = ['step_4']) 

# Plot Results
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Plot Results for step_2
rhino.plot_data(mdl, lstep='step_4', field='uz', cbar_size=1, source='linel')
#rhino.plot_data(mdl, lstep='step_4', field='sf1', cbar_size=1, source='linel')
#rhino.plot_data(mdl, lstep='step_4', field='sf2', cbar_size=1, source='linel')
#rhino.plot_data(mdl, lstep='step_4', field='sf3', cbar_size=1, source='linel')
#rhino.plot_data(mdl, lstep='step_4', field='sf4', cbar_size=1, source='linel')
#rhino.plot_data(mdl, lstep='step_4', field='sf5', cbar_size=1, source='linel')
#rhino.plot_data(mdl, lstep='step_4', field='sm1', cbar_size=1, source='linel')
#rhino.plot_data(mdl, lstep='step_4', field='sm2', cbar_size=1, source='linel')
#rhino.plot_data(mdl, lstep='step_4', field='sm2', cbar_size=1, source='linel')
#rhino.plot_data(mdl, lstep='step_4', field='sm3', cbar_size=1, source='linel')
