
from compas_fea.structure import Structure
from strucenglib.prepost_functions import plot_loc_axes
from strucenglib.prepost_functions import add_loc_coor


# Struktur bestimmen
name = 'Rahmen'
path = 'C:\Temp\\'
mdl = Structure(name=name, path=path)

# Input
PORIG=[[0,0,3120],[10000,0,0],[0,0,0]]
PXAXS=[[1,0.5,0],[0,1,0],[0,1,0]]
layers=['elset_deck','elset_wall_right','elset_wall_left']

# Call plot function
plot_loc_axes(mdl,layers=layers, PORIG=PORIG, PXAXS=PXAXS, axes_scale=200) 






