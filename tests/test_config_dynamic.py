""" Prueba Unitaria de Configuración Dínamica"""

# pyright: reportUnusedImport=false

# pylint: disable=import-outside-toplevel
# pylint: disable=unused-import

class TestConfigDynamic:
    """Clase de Pruebas Unitarias de Configuración Dínamica"""

    def test_imports(self):
        """ Prueba Unitaria Importación de Módulo - Configuración"""
        import villapy.config
        import villapy.config.dynamic

    def test_base_path(self):
        """ Prueba Unitaria de la función config_base_path"""
        from villapy.config.dynamic import config_base_path
        from villapy.config.static import di_config

        st_test = "data/"
        config_base_path(st_test)
        assert di_config["base_path"] == st_test

    def test_final_path(self):
        """ Prueba Unitaria de la función config_final_path"""
        from villapy.config.dynamic import config_final_path
        from villapy.config.static import di_config

        st_test = "data/"
        config_final_path(st_test)
        assert di_config["final_path"] == st_test

# finite Incantatem
