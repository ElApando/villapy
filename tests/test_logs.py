"""Pruebas unitarias para utilidades de sistema de archivos."""

# pyright: reportPrivateUsage=false
# pyright: reportArgumentType=false
# pylint: disable=protected-access

import datetime
from pathlib import Path

from villapy_lib.looging.write_log import WriteLogs 
from villapy_lib.config.dynamic import config_base_path

class TestLog:
    """ Prueba Uniatria de registro """

    def test_log(self, tmp_path: Path):
        """ Prueba Unitaria de registros """

        logs_dir = tmp_path / "logs"
        config_base_path(tmp_path)
        logs_dir.mkdir(parents=True, exist_ok=True)

        log = WriteLogs()
        log.write_logs(st_text = "mensaje-prueba")
        log.logs_with_name(st_name_rate="pipeline", st_text="mensaje-prueba")

        st_daily_file = logs_dir / f"logs_{datetime.datetime.now().date()}.txt"
        st_named_file = logs_dir / "logs_pipeline.txt"

        assert st_daily_file.exists()
        assert "mensaje-prueba" in st_daily_file.read_text(encoding="utf-8")

        assert st_named_file.exists()
        assert "mensaje-prueba" in st_named_file.read_text(encoding="utf-8")

# Finite Incantatem
