""" Prueba Unitaria de importaciones de módulos """

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnusedImport=false

# pylint: disable=unused-import
# pylint: disable=import-outside-toplevel

class TestImportModuls:
    """ Clase de Pruebas de Unitarias de Importar Módulos"""

    def test_imports_library(self):
        """ Prueba Unitaria Importación de Módulo - Libreria"""
        import villapy

    def test_imports_dependencies(self):
        """ Prueba Unitaria Importación de Módulo - Dependencias"""
        import villapy.cloud
        import villapy.config
        import villapy.data
        import villapy.database
        import villapy.filesystem
        import villapy.looging
        import villapy.utils

    def test_imports_cloud(self):
        """ Prueba Unitaria Importación de Módulo - Nube"""
        import villapy.cloud.azure
        import villapy.cloud.google

    def test_imports_config(self):
        """ Prueba Unitaria Importación de Módulo - Configuración"""
        import villapy.config.dynamic
        import villapy.config.static

    def test_imports_data(self):
        """ Prueba Unitaria Importación de Módulo - Datos"""
        import villapy.data.dataframe
        import villapy.data.text

    def test_imports_database(self):
        """ Prueba Unitaria Importación de Módulo - Base de Datos"""
        import villapy.database.connection
        import villapy.database.query
        import villapy.database.sqlite

    def test_imports_filesystem(self):
        """ Prueba Unitaria Importación de Módulo - Sistema de Archivos"""
        import villapy.filesystem.files_utils
        import villapy.filesystem.mapper
        import villapy.filesystem.path_utils

# Finite Incantatem
