"""Pruebas unitarias para extracción desde SQLite."""

# pyright: reportSelfClsParameterName=false

# pylint: disable=missing-class-docstring
# pylint: disable=import-outside-toplevel

from pathlib import Path
import sqlite3
import pytest

class TestSQLite:
    """ Prueba unitaria SQLite"""

    def test_sqlite_extract(self, tmp_path: Path):
        """Prueba Unitaria de la extracción de tablas de SQLite"""
        pytest.importorskip("pandas")

        from villapy_lib.database.sqlite import MangeSqlite

        db_path = tmp_path / "sample.db"
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
        conn.execute("INSERT INTO users VALUES (1, 'Ana')")
        conn.commit()
        conn.close()

        manager = MangeSqlite()
        data = manager.extract_tables_sqlite(db_path)

        assert "users" in data
        assert list(data["users"].columns) == ["id", "name"]
        assert data["users"].iloc[0]["name"] == "Ana"

# Finite Incantatem
