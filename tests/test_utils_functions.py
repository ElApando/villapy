""" Prueba Uniataria Mapeador """

# pyright: reportRedeclaration = false
# pyright: reportUnknownParameterType = false
# pyright: reportMissingParameterType = false
# pyright: reportUnknownMemberType = false
# pyright: reportArgumentType = false
# pyright: reportPrivateUsage = false
# pyright: reportUnknownVariableType = false

# pylint: disable=protected-access
# pylint: disable=broad-exception-raised

from pathlib import Path

from villapy_lib.utils.functions import ManageFunctios
from villapy_lib.config.dynamic import config_base_path

class TestMapper:
    """ Prueba Uniataria Mapeador """

    def function_prove_1(self):
        """ Funcion Erronea"""
        raise Exception("Error")

    def function_prove_2(self):
        """ Fucnión Correcta """
        return "OK"

    def test_function_fail(self, tmp_path: Path):
        """ Prueba Uniataria Mapeador - Ruta no valida """
        config_base_path(tmp_path)
        logs_dir = tmp_path / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        active = ManageFunctios()
        result = active.retry_function(function=self.function_prove_1, st_site="prueba")

        assert result == "fail"

    def test_function_true(self, tmp_path: Path):
        """ Prueba Uniataria Mapeador - Ruta no valida """
        config_base_path(tmp_path)
        logs_dir = tmp_path / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        active = ManageFunctios()
        result = active.retry_function(self.function_prove_2, "prueba")

        assert result == "OK"

    def test_function_run(self, tmp_path: Path, capsys):
        """ Prueba Uniataria Mapeador - Ruta no valida """
        config_base_path(tmp_path)
        logs_dir = tmp_path / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        active = ManageFunctios()
        active.run_stage(st_name_process="prueba", fu_function=self.function_prove_2)
        captured = capsys.readouterr()

        assert not "Fallo el proceso" in captured.out

# Finite Incantatem
