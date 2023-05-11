from aiida.plugins import WorkflowFactory, DataFactory
from aiida import load_profile
from ase.io import read
import os
from aiida.orm import Group, CalcJobNode, QueryBuilder, WorkChainNode
load_profile()

UpfData = DataFactory('core.upf')
pseudo_set = Group

pseudos = {
    "core_hole_paw",
    "gipaw_paw",
           }
path = f"/home/jovyan/work/pseudo/michael/c_o_f_si"
# loop all files in path, if file ends with .UPF, store it
corr = {"C_1s": {"core": 345.99, "exp": 6.2},
        "O_1s": {"core": 676.47, "exp": 8.25},
        "F_1s": {"core": 964.49, "exp": 8.76},
        "Si_2p": {"core": 153.76, "exp": 0.57},
        "Pt_4p": {"core": 248.14, "exp": 0},
        }

for file in os.listdir(path):
    if file.endswith(".UPF"):
        label = file.split(".")[0]
        ch = file.split(".")[1]
        if ch.startswith("star"):
            orbital = ch[4:]
        else:
            orbital = 'gs'
        pseudo = UpfData(os.path.join(path, file))
        label = f"{label}_{orbital}"
        pseudo.label = label
        pseudo.store()
        print(f"{label}: {pseudo.pk}")
        group = (
            QueryBuilder()
            .append(pseudo_set, filters={"label": "xps_pseudo_demo"})
            .one()[0]
        )
        group.add_nodes(pseudo)
group.base.extras.set("correction", corr)
