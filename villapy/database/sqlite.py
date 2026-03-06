"""
Docstring for database.sqlite
"""

from pathlib import Path
from typing import Dict, List

import pandas as pd
import sqlite3

class MangeSqlite:
    """ DOC """

    def __init__(self) -> None:
        """
        Docstring for __init__
        """
        pass

    def extract_tables_sqlite(self, st_path:Path)->Dict[str, pd.DataFrame]:
        """ extract_tables_sqlite
        
        Parameters:
            pa_path (Path): Ruta del archivo

        Returns:
            di_tables (Dict): Diccionario con los datos de las tablas SQL
        """
        di_tables: Dict[str, pd.DataFrame] = {}

        conection = sqlite3.connect(st_path)
        ls_tables: List[str] = pd.read_sql(  # type: ignore
        "SELECT name FROM sqlite_master WHERE type='table';", conection)["name"].tolist()

        for table in ls_tables:
            df_data = pd.read_sql_query(f"SELECT * FROM {table}",conection) # type: ignore
            di_tables[table] = df_data

        conection.close()

        return di_tables

# Finite Incantatem
