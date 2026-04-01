""" Prueba Unitaria de Tablas Pandas

CPH:

Limpieza de nombre y apellidos sin Numeros ni caracteres extraños 
"""

# pyright: reportUnusedImport=false

# pylint: disable=import-outside-toplevel
# pylint: disable=unused-import

class TestDataDataFrame:
    """Clase de Pruebas Unitarias de Configuración Estática"""

    def test_imports(self):
        """ Prueba Unitaria Importación de Módulo - Configuración"""
        import villapy_lib.data
        import villapy_lib.data.dataframe

    def test_format_column(self):
        """ Prueba Unitaria de la función config_base_path"""
        import pandas as pd
        from villapy_lib.data.dataframe import ManageTable

        activate = ManageTable()

        df_data = pd.DataFrame({"fecha": 
                                ["2025-10-22", "2025/10/22", "2025-22-10", "10-22-2025", "", ],
                                "hora": ["10:12", "10:w2:00", "10:12:", "1:12:00", "", ],
                                "nombre": ["juan", "roberto", "claudio", "!211124", "", ],
                                "apellido": ["gonzalez", "fernadez", "carmen", "cebolla","", ],
                                "edad": ["12", "2.5", "3e", 59.6, "", ],
                                "cantidad": ["12.456", 23.345, "123r.", 56, "", ]})

        df_data = activate.format_column(df_data, ["fecha"], "date")
        df_data = activate.format_column(df_data, ["hora"], "time")
        df_data = activate.format_column(df_data, ["nombre", "apellido"], "str")
        df_data = activate.format_column(df_data, ["edad"], "int")
        df_data = activate.format_column(df_data, ["cantidad"], "float")

        assert str(df_data["fecha"][0]) == "2025-10-22 00:00:00"
        assert str(df_data["hora"][0]) == "10:12:00"
        assert df_data["nombre"][0] == "JUAN"
        assert df_data["apellido"][0] == "GONZALEZ"
        assert df_data["edad"][0] == 12
        assert df_data["cantidad"][0] == 12.456

# finite Incantatem
