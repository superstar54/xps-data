import os

# I want to loop all the file with .UPF extension in the "PP_and_corrections" folder
cwd = os.getcwd()
core_hole = {}
gipaw = {}
pp_folder = "PP_and_corrections"
for filename in os.listdir(pp_folder):
    if filename.endswith(".UPF"):
        print(os.path.join("PP_and_corrections", filename))
        data = filename.split(".")
        if data[1].startswith("star"):
            core_hole[data[0]] = os.path.join(cwd, pp_folder, filename)
        else:
            gipaw[data[0]] = os.path.join(cwd, pp_folder, filename)
    else:
        continue

print(core_hole)
print(gipaw)

from aiida.plugins import DataFactory
from aiida import load_profile
from ase.io import read
from aiida.orm import Group, QueryBuilder
load_profile()

UpfData = DataFactory('core.upf')
pseudo_set = Group

pseudos = {
    "core_hole": core_hole,
    "gipaw": gipaw,
           }
for label in pseudos:
    group = (
            QueryBuilder()
            .append(pseudo_set, filters={"label": label})
            .one()[0]
        )
    for ele, file in pseudos[label].items():
        pseudo = UpfData(file)
        pseudo.store()
        group.add_nodes(pseudo)
        print(f"{ele}: {pseudo.pk}")
