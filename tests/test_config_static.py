""" Prueba Unitaria de Configuración Estática"""

# pyright: reportUnusedImport=false

# pylint: disable=import-outside-toplevel
# pylint: disable=unused-import

class TestConfigStatic:
    """Clase de Pruebas Unitarias de Configuración Estática"""

    def test_imports(self):
        """ Prueba Unitaria Importación de Módulo - Configuración"""
        import villapy.config
        import villapy.config.static

    def test_config_di_config(self):
        """ Prueba Unitaria de la función config_base_path"""
        from villapy.config.static import di_config

        assert isinstance(di_config, dict)
        assert "base_path" in  di_config
        assert "final_path" in  di_config

# finite Incantatem
