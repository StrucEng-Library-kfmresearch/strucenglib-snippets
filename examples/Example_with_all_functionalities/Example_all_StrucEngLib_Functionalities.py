
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
name = 'Nachweisschnitt'
path = 'C:\Temp\\'
mdl = Structure(name=name, path=path)

# Structure
mdl = Structure(name=name, path=path)

# Shell Elements
rhino.add_nodes_elements_from_layers(mdl, mesh_type='ShellElement', layers=[ 'elset_deck', 'elset_wall_right', 'elset_wall_left'] ) 

# MPC Elements
rhino.add_nodes_elements_from_layers(mdl, line_type='MPCElement', layers='elset_mpc')

# Sets for constraints
rhino.add_sets_from_layers(mdl, layers=[ 'nset_pinned' ] )

# Shell Materials
mdl.add(ElasticIsotropic(name='elset_deck_element_mat', E=33700, v=0.0, p=2100/10**9)) # for layer: elset_deck
mdl.add(ElasticIsotropic(name='elset_wall_right_element_mat', E=30000, v=0.1, p=2200/10**9)) # for layer: elset_wall_right
mdl.add(ElasticIsotropic(name='elset_wall_left_element_mat', E=35000, v=0.2, p= 2300/10**9)) # for layer: elset_wall_left

# MPC Materials
mdl.add(MPCStiff(name='elset_mpc_element_mat'))

# Shell Sections, Properties, additional Properties, set local coordiantes (The local z-axed is adjusted by using "object direction" in Rino) 
data = {}
semi_loc_coords=calc_loc_coor(layer='elset_deck', PORIG=[0,0,2980],PXAXS=[1,0,0]) 
mdl.add(ShellSection(name='elset_deck_element_sec', t=200, semi_loc_coords=semi_loc_coords)) # global Coordiantes
mdl.add(Properties(name='elset_deck_element_prop', material='elset_deck_element_mat', section='elset_deck_element_sec', elset='elset_deck'))
SMM.additionalproperty(data, prop_name='elset_deck_element_prop', d_strich_bot = 40, d_strich_top = 40, fc_k = 20, theta_grad_kern = 45, fs_d = 435, alpha_bot = 0, beta_bot = 90, alpha_top = 0, beta_top = 90, ex=semi_loc_coords[4], ey=semi_loc_coords[5], ez=semi_loc_coords[6])

semi_loc_coords =calc_loc_coor(layer='elset_wall_right', PORIG=[0,5400,0],PXAXS=[1,0,0]) 
mdl.add(ShellSection(name='elset_wall_right_element_sec', t=200, semi_loc_coords=semi_loc_coords)) # global Coordiantes
mdl.add(Properties(name='elset_wall_right_element_prop', material='elset_wall_right_element_mat', section='elset_wall_right_element_sec', elset='elset_wall_right'))
SMM.additionalproperty(data, prop_name='elset_wall_right_element_prop', d_strich_bot = 40, d_strich_top = 40, fc_k = 20, theta_grad_kern = 45, fs_d = 435, alpha_bot = 0, beta_bot = 90, alpha_top = 0, beta_top = 90, ex=semi_loc_coords[4], ey=semi_loc_coords[5], ez=semi_loc_coords[6])
 
semi_loc_coords =calc_loc_coor(layer='elset_wall_left', PORIG=[0,0,0],PXAXS=[1,0,0])   
mdl.add(ShellSection(name='elset_wall_left_element_sec', t=200, semi_loc_coords=semi_loc_coords)) # global Coordiantes
mdl.add(Properties(name='elset_wall_left_element_prop', material='elset_wall_left_element_mat', section='elset_wall_left_element_sec', elset='elset_wall_left'))
SMM.additionalproperty(data, prop_name='elset_wall_left_element_prop', d_strich_bot = 40, d_strich_top = 40, fc_k = 20, theta_grad_kern = 45, fs_d = 435, alpha_bot = 0, beta_bot = 90, alpha_top = 0, beta_top = 90, ex=semi_loc_coords[4], ey=semi_loc_coords[5], ez=semi_loc_coords[6])

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
loaded_element_numbers=area_load_generator_elements(mdl,layer='area_load') 
mdl.add(AreaLoad(name='area_load', elements=loaded_element_numbers,x=0,y=0,z=-0.00625*400)) 

# Normalspurverkehr Load generator
return_values_Gleis_1=Normalspurbahnverkehr_load_generator(mdl,name='Gleis_1', l_Pl=5400, h_Pl=200, s=4500, beta=-30, q_Gl=-0.8*10000, b_Bs=1000, h_Strich=200, Q_k=-2.25*1000, y_A=2000)


# Steps
mdl.add([
GeneralStep(name='step_1',   displacements=[ 'nset_pinned_set_disp' ] ,  nlgeom=False),
GeneralStep(name='step_2',  loads=['load_gravity'] ,   nlgeom=False),
GeneralStep(name='step_3',  loads=['area_load'] ,   nlgeom=False),
GeneralStep(name='step_4',  loads=return_values_Gleis_1 ,   nlgeom=False),
])
mdl.steps_order = [ 'step_1', 'step_2', 'step_3' , 'step_4'  ]  

# Nachweisschnitte (Querkraft)
verification(mdl,layer='verification_V_deck', check='V')



# Run analyses
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
mdl.analyse_and_extract(software='ansys_sel', fields=[ 'u', 'sf' ], lstep = ['step_2','step_3','step_4']) 
SMM.Hauptfunktion(structure = mdl, data = data, lstep = ['step_2','step_3','step_4'], Mindestbewehrung = False, Druckzoneniteration = True, Schubnachweis = 'sia', code = 'sia', axes_scale = 100)



# Plot Results
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Plot linear elastic results
rhino.plot_data(mdl, lstep='step_3', field='ux', cbar_size=1, source='linel')
rhino.plot_data(mdl, lstep='step_2', field='uy', cbar_size=1, source='linel')
rhino.plot_data(mdl, lstep='step_2', field='uz', cbar_size=1, source='linel')
rhino.plot_data(mdl, lstep='step_3', field='uz', cbar_size=1, source='linel')
rhino.plot_data(mdl, lstep='step_4', field='uz', cbar_size=1, source='linel')
rhino.plot_data(mdl, lstep='step_2', field='sf1', cbar_size=1, source='linel')
rhino.plot_data(mdl, lstep='step_2', field='sf2', cbar_size=1, source='linel')
rhino.plot_data(mdl, lstep='step_2', field='sf3', cbar_size=1, source='linel')
rhino.plot_data(mdl, lstep='step_2', field='sf4', cbar_size=1, source='linel')
rhino.plot_data(mdl, lstep='step_2', field='sf5', cbar_size=1, source='linel')
rhino.plot_data(mdl, lstep='step_2', field='sm1', cbar_size=1, source='linel')
rhino.plot_data(mdl, lstep='step_2', field='sm2', cbar_size=1, source='linel')
rhino.plot_data(mdl, lstep='step_2', field='sm3', cbar_size=1, source='linel')


# Plot Sandwichmodel
rhino.plot_data(mdl, lstep='step_2', field='as_xi_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_3', field='as_xi_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_4', field='as_xi_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_2', field='as_eta_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_3', field='as_eta_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_4', field='as_eta_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_2', field='as_xi_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_3', field='as_xi_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_4', field='as_xi_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_2', field='as_eta_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_3', field='as_eta_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_4', field='as_eta_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_2', field='as_z', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_2', field='CC_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_2', field='CC_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_2', field='k_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_2', field='k_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_2', field='t_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_2', field='t_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_2', field='psi_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_2', field='psi_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_2', field='Fall_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_2', field='Fall_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_2', field='m_cc_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_2', field='m_cc_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_2', field='m_shear_c', cbar_size=1, source='SMM')
rhino.plot_data(mdl, lstep='step_2', field='m_c_total', cbar_size=1, source='SMM')