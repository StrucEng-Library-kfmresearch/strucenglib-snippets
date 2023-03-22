
# This is auto generated code by StrucEngLib Plugin 0.0.11
# Find source at https://github.com/kfmResearch-NumericsTeam/StrucEng_Library_Plug_in
# Code generated at 2022-08-31T14:51:26.8110673+02:00
# Issued by user mariuweb

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
from strucenglib.sandwichmodel import sandwichmodel_main as SMM

# Initialisieren
name = 'Example_area_load_generator_elements'
path = 'C:\Temp\\'
mdl = Structure(name=name, path=path)

# Structure
mdl = Structure(name=name, path=path)

# Elements
rhino.add_nodes_elements_from_layers(mdl, mesh_type='ShellElement', layers='elset_mesh')

# Sets for constraints
rhino.add_sets_from_layers(mdl, layers=['nset_left', 'nset_right', 'nset_up'])

# Materials
mdl.add(ElasticIsotropic(name='mat_elastic', E=33700, v=0.2, p=2500/10**9))

# Shell Sections, Properties, additional Properties, set local coordiantes (The local z-axed is adjusted by using "object direction" in Rino) 
data = {}
semi_loc_coords=calc_loc_coor(layer='elset_mesh', PORIG=[0,0,0],PXAXS=[1,0,0]) 
mdl.add(ShellSection(name='sec_plate', t=300, semi_loc_coords=semi_loc_coords)) # global Coordiantes
mdl.add(Properties(name='ep_plate', material='mat_elastic', section='sec_plate', elset='elset_mesh'))
SMM.additionalproperty(data, prop_name='ep_plate', d_strich_bot = 40, d_strich_top = 40, fc_k = 30, theta_grad_kern = 45, fs_d = 435, alpha_bot = 0, beta_bot = 90, alpha_top = 0, beta_top = 90, ex=semi_loc_coords[4], ey=semi_loc_coords[5], ez=semi_loc_coords[6])

# Displacements
mdl.add([
    PinnedDisplacement(name='disp_left', nodes='nset_left'),
    RollerDisplacementX(name='disp_right', nodes='nset_right'),
    RollerDisplacementXZ(name='disp_up', nodes='nset_up'),
])

# Area Load generator
loaded_element_numbers=area_load_generator_elements(mdl,layer='area_load') # Calculate Element numbers within the area load curve
mdl.add(AreaLoad(name='area_load_pressure', elements=loaded_element_numbers,x=0,y=-0.625*400,z=0)) # Add new element set, load in N/mm2 in local y direction

# Steps
mdl.add([
    GeneralStep(name='step_1', displacements=['disp_left', 'disp_right', 'disp_up'],nlgeom=False),
    GeneralStep(name='step_2', loads=['area_load_pressure'], increments=1, nlgeom=False),
])
mdl.steps_order = ['step_1', 'step_2']


# Run
mdl.analyse_and_extract(software='ansys_sel', fields=[ 'u', 'sf' ] )

# Plot Step step_2
rhino.plot_data(mdl, step='step_2', field='ux', cbar_size=1)
rhino.plot_data(mdl, step='step_2', field='uy', cbar_size=1)
rhino.plot_data(mdl, step='step_2', field='uz', cbar_size=1)
rhino.plot_data(mdl, step='step_2', field='um', cbar_size=1)
rhino.plot_data(mdl, step='step_2', field='sf1', cbar_size=1)
rhino.plot_data(mdl, step='step_2', field='sf2', cbar_size=1)
rhino.plot_data(mdl, step='step_2', field='sf3', cbar_size=1)
rhino.plot_data(mdl, step='step_2', field='sf4', cbar_size=1)
rhino.plot_data(mdl, step='step_2', field='sf5', cbar_size=1)
rhino.plot_data(mdl, step='step_2', field='sm1', cbar_size=1)
rhino.plot_data(mdl, step='step_2', field='sm2', cbar_size=1)
rhino.plot_data(mdl, step='step_2', field='sm3', cbar_size=1)
#
## SM for step_2
SMM.Hauptfunktion(structure = mdl, data = data, step = 'step_2', Mindestbewehrung = True, Druckzoneniteration = True, Schubnachweis = 'sia', code = 'sia', axes_scale = 100)
rhino.plot_data(mdl, step='step_2', field='as_xi_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, step='step_2', field='as_xi_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, step='step_2', field='as_eta_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, step='step_2', field='as_eta_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, step='step_2', field='as_z', cbar_size=1, source='SMM')
rhino.plot_data(mdl, step='step_2', field='CC_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, step='step_2', field='CC_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, step='step_2', field='k_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, step='step_2', field='k_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, step='step_2', field='t_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, step='step_2', field='t_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, step='step_2', field='psi_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, step='step_2', field='psi_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, step='step_2', field='Fall_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, step='step_2', field='Fall_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, step='step_2', field='m_cc_bot', cbar_size=1, source='SMM')
rhino.plot_data(mdl, step='step_2', field='m_cc_top', cbar_size=1, source='SMM')
rhino.plot_data(mdl, step='step_2', field='m_shear_c', cbar_size=1, source='SMM')
rhino.plot_data(mdl, step='step_2', field='m_c_total', cbar_size=1, source='SMM')