# Author(s): Marius  Weber (ETHZ, HSLU T&A)

from compas_fea.structure import Structure
from strucenglib.prepost_functions import plot_nr_elem


# Struktur bestimmen
name = 'Rahmen'
path = 'C:\Temp\\'
mdl = Structure(name=name, path=path)

# Import semi local coordinate systems 
plot_nr_elem(mdl,layers=['elset_deck','elset_wall_left','elset_wall_right'])

