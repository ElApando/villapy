"""Pruebas unitarias para utilidades de sistema de archivos."""

# pyright: reportPrivateUsage=false
# pylint: disable=protected-access

import json
from pathlib import Path

from villapy.filesystem.files_utils import OpenFiles, ManageFile
from villapy.config.dynamic import config_base_path

class TestManageFile:
    """ Prueba Uniatria Manejo de Archivos """

    def test_open_json(self, tmp_path: Path):
        """ Prueba Unitaria apertura de json"""
        payload = {"a": "1", "b": "2"}
        json_path = tmp_path / "data.json"
        json_path.write_text(json.dumps(payload), encoding="utf-8")

        activate = OpenFiles()
        assert activate.open_json(str(json_path)) == payload

    def test_separator_what(self):
        """ Prueba Unitaria que separador tienen los datos """
        config_base_path("")
        manager = ManageFile()
        assert manager._separator_what("a|b|c") == "|"
        assert manager._separator_what("a;b;c") == ";"
        assert manager._separator_what("a\tb\tc") == "\t"
        assert manager._separator_what("a,b,c") == ","

    def test_separator_table(self, tmp_path: Path):
        """ Prueba Unitaria lee la primera linea y obtiene el separador """
        path = tmp_path / "table.csv"
        path.write_text("c1;c2\n1;2\n", encoding="utf-8")
        config_base_path("")
        manager = ManageFile()

        assert manager.separator_table(path) == ";"


    def test_move_file_copy_and_cut(self, tmp_path: Path):
        """ Prueba Unitaria Copia o Corta Archivos """
        config_base_path("")
        manager = ManageFile()
        source = tmp_path / "source.txt"
        source.write_text("hola", encoding="utf-8")

        copy_dest = tmp_path / "copied.txt"
        manager.move_file(source, copy_dest, "COPY")
        assert source.exists()
        assert copy_dest.read_text(encoding="utf-8") == "hola"

        cut_dest = tmp_path / "moved.txt"
        manager.move_file(source, cut_dest, "CUT")
        assert not source.exists()
        assert cut_dest.exists()

# Finite Incantatem
