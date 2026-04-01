
""" Prueba Unitaria Conexión a la Base de Datos se cree correctamente
python -m tests.test_database_query
"""

# pyright: reportUnusedImport=false
# pyright: reportUnknownMemberType=false
# pyright: reportMissingParameterType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownVariableType=false

# pylint: disable=missing-class-docstring
# pylint: disable=import-outside-toplevel


from datetime import date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import pytest
import pandas as pd

class Base(DeclarativeBase):
    pass


class ModelDataBaseTable(Base):
    """ Módelo de prueba """
    __tablename__ = "test_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date]
    brand: Mapped[str]


class TestDataBase:
    """ Prueba Unitaria de la Base de Datos """

    @pytest.fixture
    def db(self):
        """Fixture conexión a la base de datos de pruebas"""
        from villapy_lib.database.query import QuerysDB
        active_db = QuerysDB(
            {"username": "", "password": "", "server": ""}, True)
        return active_db

    @pytest.fixture
    def df_upload(self):
        """Dataframe 1 de pruebas"""
        df_data = pd.DataFrame({"id": [1,2,3,4,5,6],
                                "date": ["10/03/2026", "10/03/2026", "10/03/2026",
                                         "10/03/2026", "10/03/2026", "11/03/2026"],
                                "brand": ["a", "b", "c", "d", "e", "g"]})
        return df_data

    @pytest.fixture
    def df_append(self):
        """Dataframe 2 de pruebas"""
        df_data = pd.DataFrame({"id": [6],
                                "date": ["2026-10-03"],
                                "brand": ["f"]})
        return df_data

    def test_create(self, db):
        """ Prueba Uniataria Creación de una tabla """
        db.database_tbl_create(model=ModelDataBaseTable)
        ls_tables = db.database_name_tables()
        assert "test_table" in ls_tables

    def test_upload_select(self, db, df_upload):
        """ Prueba Unitaria de Actualización y Selección de datos """

        db.database_df_upload(model=ModelDataBaseTable, df_data = df_upload)
        df_data = db.database_df_select(st_name_table = "test_table")
        assert df_data["id"][0] == 1
        assert df_data["date"][0] == "10/03/2026"
        assert df_data["brand"][0] == "a"

    def test_append_select(self, db, df_append):
        """ Agregación de un registro a una tabla"""

        db.database_df_append(model=ModelDataBaseTable, df_data = df_append)
        df_data = db.database_df_select(st_name_table = "test_table")
        assert df_data["id"][0] == 6
        assert str(df_data["date"][0]) == "2026-10-03 00:00:00"
        assert df_data["brand"][0] == "f"

    def test_delete_v1(self, db, df_upload):
        """ Eliminación de registros tipo 1  """
        da_date = pd.to_datetime("10/03/2026", format  ="%d/%m/%Y").date()
        df_upload["date"] = pd.to_datetime(df_upload["date"], format="%d/%m/%Y").dt.date
        db.database_df_append(model=ModelDataBaseTable, df_data = df_upload)
        db.database_data_delete(model=ModelDataBaseTable, st_date_current = da_date,
                                st_brand_name = "b")
        df_data = db.database_df_select(st_name_table = "test_table")
        assert (df_data["date"].dt.date == da_date).any()
        assert not "b" in df_data["date"].values

    def test_delete_v2(self, db, df_upload):
        """ Eliminación de registros tipo 2 """
        da_date = pd.to_datetime("10/03/2026", format  ="%d/%m/%Y").date()
        df_upload["date"] = pd.to_datetime(df_upload["date"], format="%d/%m/%Y").dt.date
        db.database_df_append(model=ModelDataBaseTable, df_data = df_upload)
        db.database_data_delete_v2(model=ModelDataBaseTable, st_date_current = da_date,
                                st_brand_name = "b", st_column = "brand")
        df_data = db.database_df_select(st_name_table = "test_table")
        assert (df_data["date"].dt.date == da_date).any()
        assert not "b" in df_data["date"].values

    def test_delete_v3(self, db, df_upload):
        """ Eliminación de registros tipo 3 """
        da_date = pd.to_datetime("10/03/2026", format  ="%d/%m/%Y").date()
        df_upload["date"] = pd.to_datetime(df_upload["date"], format="%d/%m/%Y").dt.date
        db.database_df_append(model=ModelDataBaseTable, df_data = df_upload)
        db.database_data_delete_v3(model=ModelDataBaseTable, st_date_current = da_date)
        df_data = db.database_df_select(st_name_table = "test_table")
        assert not (df_data["date"].dt.date == da_date).any()
        assert not "b" in df_data["date"].values

# Finite Incantatem
