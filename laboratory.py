""" Laboratorio """

import os
from filesystem.mapper import ManageFolder

st_path_origin = os.getcwd()
st_active = ManageFolder(st_path=st_path_origin, st_env="villa_env")
st_active.execute()

# Finite Incatatem
