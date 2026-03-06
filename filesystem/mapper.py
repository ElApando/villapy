"""
Docstring for mapper

Este programa se hará como una herramienta extra
\t
"""

import os
from typing import List

class ManageFolder:
    """ DOC """

    def __init__(self, st_path: str = "", st_env: str|None = None,
                 ls_ignore: List[str]|None = None):
        """ DOC
        """
        self.st_path = st_path
        self.st_env = st_env
        self.ls_base_ignore: List[str] = [".git", "__pycache__", ".gitignore"]
        self.st_separator = "  "
        ls_ignore = ls_ignore or []

        if self.st_env:
            self.ls_base_ignore.append(self.st_env)

        self.ls_ignore: List[str] = self.ls_base_ignore + ls_ignore


    def execute(self):
        """ DOC """

        self.mapper(self.st_path)


    def mapper(self, st_path:str, in_depth: int = 0):
        """ DOC """
        st_tabulate = f"|{self.st_separator}" * in_depth
        ls_folder = self.test_secure(st_path, st_tabulate)

        for folder in ls_folder:
            if folder in self.ls_ignore:
                continue

            print(f"{st_tabulate}| - {folder}")
            full_path: str = os.path.join(st_path, folder)

            if os.path.isdir(full_path):
                self.mapper(full_path, in_depth= in_depth + 1)


    def test_secure(self, st_path:str, st_tabulate:str)->List[str]:
        """ Doc """
        try:
            ls_folder = os.listdir(st_path)

        except PermissionError:
            print(f"{st_tabulate} - [Sin Permisos]")
            return []

        except FileNotFoundError:
            print(f"{st_tabulate} - [Ruta No Encontrada]")
            return []

        return ls_folder

# Finite Incantatem
