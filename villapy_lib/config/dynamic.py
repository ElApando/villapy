
""" Configuración Dinamica del Proyecto """

from pathlib import Path

from villapy_lib.config.static import di_config

def config_base_path(base_path:Path):
    """ Configuración del Path """
    di_config["base_path"] = base_path

def config_final_path(final_path:Path):
    """ Configuración del Path """
    di_config["final_path"] = final_path

# Finite Incantatem
