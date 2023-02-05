
from compas_fea.cad import rhino
from compas_fea.structure import ElasticIsotropic
from compas_fea.structure import ElementProperties as Properties
from compas_fea.structure import GeneralDisplacement
from compas_fea.structure import GeneralStep
from compas_fea.structure import GravityLoad
from compas_fea.structure import AreaLoad
from compas_fea.structure import PointLoad
from compas_fea.structure import PinnedDisplacement
from compas_fea.structure import RollerDisplacementX
from compas_fea.structure import RollerDisplacementY
from compas_fea.structure import RollerDisplacementXY
from compas_fea.structure import ShellSection
from compas_fea.structure import Structure


import sandwichmodel_main as SMM

# Author(s): Andrew Liew (github.com/andrewliew), Benjamin Berger (github.com/Beberger)


#Allgemein
thickness_wall = 250 #mm
thickness_deck = 500 #mm
name = 'Rahmen'
path = 'C:/Temp/'
# Structure

mdl = Structure(name=name, path=path)

# Elements

rhino.add_nodes_elements_from_layers(mdl, mesh_type='ShellElement', layers=['elset_deck','elset_wall_left','elset_wall_right'])
mdl.elements[100].axes.update({'ex': [0, 0, 1], 'ey': [0, -1, 0], 'ez': [1, 0, 0]})

mdl.elements[0].axes.update({'ex': [1, 0, 0], 'ey': [0, -1, 0], 'ez': [0, 0, -1]}) # Deck
mdl.elements[200].axes.update({'ex': [0, 0, -1], 'ey': [0, -1, 0], 'ez': [-1, 0, 0]}) # 
# Sets

rhino.add_sets_from_layers(mdl, layers=['nset_pinned'])

# Materials

mdl.add(ElasticIsotropic(name='mat_elastic', E=33700, v=0.0, p=2500/10**9)) #E[N/mm2], p[kg/mm3] 

# Sections

mdl.add(ShellSection(name='sec_deck', t=thickness_deck))#[mm]
mdl.add(ShellSection(name='sec_wall_left', t=thickness_wall))#[mm]
mdl.add(ShellSection(name='sec_wall_right', t=thickness_wall))#[mm]

# Properties

mdl.add(Properties(name='ep_deck', material='mat_elastic', section='sec_deck', elset='elset_deck'))
mdl.add(Properties(name='ep_wall_left', material='mat_elastic', section='sec_wall_left', elset='elset_wall_left'))
mdl.add(Properties(name='ep_wall_right', material='mat_elastic', section='sec_wall_right', elset='elset_wall_right'))

# Additional Properties
data = {} #generiert ein leeres dictionary fuer zusaetzliche Materialkennwerte
SMM.additionalproperty(data, prop_name = 'ep_deck',  d_strich_bot = 40, d_strich_top = 40, fc_k = 30, theta_grad_kern = 45, fs_d=435, alpha_bot =0, beta_bot = 90, alpha_top =0, beta_top = 90) #zusaetzliche Materialkennwerte werden gefuellt...
SMM.additionalproperty(data, prop_name = 'ep_wall_left',  d_strich_bot = 40, d_strich_top = 40, fc_k = 20, theta_grad_kern = 45, fs_d=435, alpha_bot = 0, beta_bot = 90, alpha_top = 0, beta_top = 90) #zusaetzliche Materialkennwerte werden gefuellt...
SMM.additionalproperty(data, prop_name = 'ep_wall_right',  d_strich_bot = 40, d_strich_top = 40, fc_k = 20, theta_grad_kern = 45, fs_d=435, alpha_bot = 0, beta_bot = 90, alpha_top = 0, beta_top = 90) #zusaetzliche Materialkennwerte werden gefuellt...




# Displacements

mdl.add([
    PinnedDisplacement(name='disp_pinned', nodes='nset_pinned')
])

# Loads

mdl.add(GravityLoad(name='load_gravity', elements=['elset_deck','elset_wall_left','elset_wall_right']))
#mdl.add(PointLoad(name='load_point', nodes='nset_middle', y=0, z=-50000, x = 0))
mdl.add(AreaLoad(name='load_pressure', elements='elset_deck', z=0.03, axes='local')) #z[N/mm2] = MN/m2, hier wird die Last in Bezug auf die lokale Achsen definiert: in z Richtung positiv = nach unten bei Deck
# Steps

mdl.add([
    GeneralStep(name='step_bc', displacements=['disp_pinned'], nlgeom=False),
    GeneralStep(name='step_load', loads=['load_gravity','load_pressure'], nlgeom=False)
    ])

mdl.steps_order = ['step_bc','step_load']

# Summary

mdl.summary()

# Run

mdl.analyse_and_extract(software='abaqus', fields=['u','sf','sm'])



rhino.plot_data(mdl, step='step_load', field='sm1',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='sm2',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='sm3',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='sf4',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='sf5',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='sf1',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='sf2',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='sf3',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='um',cbar_size=1)
#print(mdl.elements[251])
#print(mdl.elements[100])
#print(mdl.elements[222])



# SM


SMM.Hauptfunktion(structure = mdl, data = data, step = 'step_load', Mindestbewehrung = False, Druckzoneniteration = True, Schubnachweis = 'sia',code = 'sia', axes_scale = 100)



rhino.plot_data(mdl, step='step_load', field='as_xi_bot', cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='as_xi_top',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='as_eta_bot',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='as_eta_top',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='as_z',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='CC_bot',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='CC_top',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='k_bot',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='k_top',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='t_bot',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='t_top',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='psi_bot',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='psi_top',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='Fall_bot',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='Fall_top',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='m_cc_bot',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='m_cc_top',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='m_shear_c',cbar_size=1)
rhino.plot_data(mdl, step='step_load', field='m_c_total',cbar_size=1)

SMM.max_values(mdl,'step_load')
"""
print(mdl.element_properties['ep_wall_left'].section)
sec_name = mdl.element_properties['ep_wall_left'].section
print(mdl.sections[sec_name])
print(mdl.sections[sec_name].geometry['t'])
print(type(mdl.sections[sec_name].geometry['t']))
"""