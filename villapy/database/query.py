""" Compendio de querys
El archivo tiene como finalidad albergar todos los querys que se utilizan a lo largo del
código, es importante que son querys que solo funcionan para lo que fueron creados por lo
que no se crearon de forma general.

Se ejecuta con -> python -m src.query.query_sql
"""
# pylint: disable=import-error
# pylint: disable=no-name-in-module
# pylint: disable=reportMissingImports

from typing import Type, List, Dict, Callable
from datetime import date

import pandas as pd
# import pyodbc
from sqlalchemy import text, inspect, delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase

from villapy.database.connection import Connection

class QuerysDB:
    """Clase peticiones a SQL con SQLAlchemy ORM"""

    def __init__(self, di_connection:Dict[str, str])->None:
        """ Inicio de la clase

        Se hace la conexión con la base de datos, también la clase contiene diferentes peticiones 
        a la base de datos

        - Creación de base de datos
        - Subida de tablas remplazando la anterior
        - Subida de tablas agregndo información
        - Selección de tablas 
        - Eliminación de renglones 
        - Modificación del formato de las columnas
        - Nombre de las tablas ubicadas en la base de datos  
        """
        active_connection = Connection(di_connection)
        du_both = active_connection.connect_session()
        self.session = du_both[0]
        self.engines = du_both[1]
        self.st_log = "general"

    def _safe_commit(self)->None:
        """ Asegura el commit de correctamente
        
        Si el commit no funciona por alguna razón, se realiza un rollback con la finalidad
        de cuidar la integridad de los datos.
        """
        try:
            self.session.commit()

        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Error al hacer commit en DB: {e}") from e

    def _check_model(self, model:str|Type[DeclarativeBase],
            function:Callable[...,Type[DeclarativeBase]]|None=None) -> Type[DeclarativeBase]:
        """Revisión del modelo

        Si el modelo es string crea un modelo generico para poder realizar
        los cambios correspondientes en la DB
        
        Parameters:
            model (cls or str): Puede ser un string indicando el modelo que debe de ser
                creado o realmente puede ser un model pydantic
            st_type_model (str): Tipo de modelo que se quiere crear
        Returns: 
            model (cls): Modelo que será utilizado  en las peticiones 
        """
        if isinstance(model, str):
            if function is None:
                raise ValueError("Si el modelo es string ingresa la fución correspondiente")
            model = function(model)

        if not hasattr(model, "__table__"):
            print("[ERROR] El modelo no es un modelo SQLALchemy válido")
            raise TypeError("[ERROR] El modelo no es un modelo SQLALchemy válido")

        return model

    def database_tbl_create(self, model:str|Type[DeclarativeBase], 
                            function:Callable[...,Type[DeclarativeBase]]|None=None)->None:
        """ Creación de la base de datos

        Parameters:
            - model *(cls or str)* - Puede ser un string indicando el modelo que debe de ser
                creado o reallmente puede ser un model pydantic
            - st_type_model *(str)* - Tipo de modelo que se quiere crear
        """
        model = model = self._check_model(model, function)
        model.__table__.create(bind=self.engines, checkfirst=True)#type:ignore

    def database_df_upload(self, model:str|Type[DeclarativeBase], df_data: pd.DataFrame,
                           function:Callable[...,Type[DeclarativeBase]]|None=None)->None:
        """ Sube datframes remplazando la tabla anterior

        Parameters:
            - model *(cls or str)* - Puede ser un string indicando el modelo que debe de ser
                creado o reallmente puede ser un model pydantic
            - st_type_model *(str)* - Tipo de modelo que se quiere crear
            - df_data *(pd.DataFrame)* - Tabla que debe de ser subida al DB
        """
        model = self._check_model(model, function)
        self.database_tbl_create(model, function)
        df_data.to_sql(model.__tablename__, con=self.engines, if_exists="replace", index=False)

    def database_df_append(self, model:str|Type[DeclarativeBase], df_data: pd.DataFrame,
                            function:Callable[...,Type[DeclarativeBase]]|None=None)->None:
        """ Sube datframes agregando los nuevos datos a la tabla anterior

        Parameters:
            - model *(cls or str)* - Puede ser un string indicando el modelo que debe de ser
                creado o reallmente puede ser un model pydantic
            - st_type_model *(str)* - Tipo de modelo que se quiere utilizar
            - df_data *(pd.DataFrame)* - Tabla que debe de ser subida al DB
        """
        model = self._check_model(model, function)
        self.database_tbl_create(model, function)
        df_data.to_sql(model.__tablename__, con=self.engines, if_exists="append", index=False)

    def database_df_select(self, model:str|Type[DeclarativeBase]="", st_name_table:str="",
                           st_date:date|str="",
                           function:Callable[...,Type[DeclarativeBase]]|None=None)->pd.DataFrame:
        """ Seleccion de los datos # Requiere ajuste

        Parameters:
            - st_name_table *(str)* - Nombre de la tabla de interés
        Returns:
            - df_data *()* - Datos extraidos de la base de datos
        """
        if  model and function:
            model = self._check_model(model, function)

        if st_date:
            query = select(model).where(model.date == st_date) #type:ignore
            df_data = pd.read_sql(query, con=self.session.bind) #type:ignore
        else:
            df_data = pd.read_sql_table(st_name_table, con=self.engines)

        return df_data

    def database_data_delete(self,  model:str|Type[DeclarativeBase], st_date_current: str,
                             st_brand_name: str,
                             function:Callable[...,Type[DeclarativeBase]]|None=None)->None:
        """ Eliminación renglones 

        Parameters:
            - model *(cls or str)* - Puede ser un string indicando el modelo que debe de ser
                creado o reallmente puede ser un model pydantic
            - st_type_model *(str)* - Tipo de modelo que se quiere utilizar
            - st_date_current *(str)* - Fecha que se dese eliminar
            - st_brand_name *(str)* - Nombre de la submarca 
        """
        model = self._check_model(model, function)

        if st_brand_name != "":
            qu_delete = delete(model).where((model.date == st_date_current) & #type:ignore
                                            (model.brand == st_brand_name)) #type:ignore
        else:
            qu_delete = delete(model).where((model.date == st_date_current)) #type:ignore

        self.session.execute(qu_delete)
        self._safe_commit()

    def database_data_delete_v2(self, model:str|Type[DeclarativeBase], st_date_current: str,
                                st_brand_name: str, st_column: str,
                                function:Callable[...,Type[DeclarativeBase]]|None=None)->None:
        """ Eliminación renglones 

        Parameters:
            - model *(cls or str)* - Puede ser un string indicando el modelo que debe de ser
                creado o reallmente puede ser un model pydantic
            - st_type_model *(str)* - Tipo de modelo que se quiere utilizar
            - st_date_current *(str)* - Fecha que se dese eliminar
            - st_brand_name *(str)* - Nombre de la submarca
            - st_column *(str)* - Nombre de la columna de interés
        """
        model = self._check_model(model, function)

        qu_delete = delete(model).where((model.date == st_date_current) & #type:ignore
                                        (getattr(model, st_column) == st_brand_name)) #type:ignore

        self.session.execute(qu_delete)
        self._safe_commit()

    def database_data_delete_v3(self,  model:str|Type[DeclarativeBase], st_date_current:str|date,
                                function:Callable[...,Type[DeclarativeBase]]|None=None)->None:
        """ Eliminación renglones 

        Parameters:
            - model *(cls or str)* - Puede ser un string indicando el modelo que debe de ser
                creado o reallmente puede ser un model pydantic
            - st_type_model *(str)* - Tipo de modelo que se quiere utilizar
            - st_date_current *(str)* - Fecha que se dese eliminar
            - st_brand_name *(str)* - Nombre de la submarca
            - st_column *(str)* - Nombre de la columna de interés
        """
        model = self._check_model(model, function)

        qu_delete = delete(model).where((model.date == st_date_current)) #type:ignore

        self.session.execute(qu_delete)
        self._safe_commit()

    def database_format_column(self, st_column_name: str)->None:
        """ Da formato a la columna de interés 

        Parameters:
            - st_column_name *(str)* - Es el nombre de la columna que se quiere formatear
        """

        inspector = inspect(self.engines)
        with self.engines.connect() as conn:
            for table_name in inspector.get_table_names():
                columns = inspector.get_columns(table_name)
                for col in columns:
                    bo_name = col['name'] == f'{st_column_name}'
                    if bo_name:
                        # write_logs(self.st_log,
                        #            f"🔧 Modificando '{st_column_name}' en tabla: {table_name}")
                        conn.execute(
                        text(f"ALTER TABLE `{table_name}` MODIFY COLUMN `{st_column_name}` VARCHAR(255);")
                )

    def database_name_tables(self)->List[str]:
        """ Obtención del nombre de las tablas presentes en la DB

        Parameters:
            - None
        Returns:
            - ls_tables *(list)* - Lista con los nombres de las tablas
        """
        inspector = inspect(self.engines)
        ls_tables = inspector.get_table_names()
        return ls_tables

# Finite incantatem
