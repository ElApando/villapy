""" Prueba Uniataria Mapeador """

# pyright: reportRedeclaration=false
# pyright: reportUnknownParameterType=false
# pyright: reportMissingParameterType=false
# pyright: reportUnknownMemberType=false
# pylint: disable=protected-access

from villapy_lib.filesystem.mapper import Mapper

class TestMapper:
    """ Prueba Uniataria Mapeador """

    def test_mapper(self, capsys):
        """ Prueba Uniataria Mapeador - Ruta no valida """
        active = Mapper(st_path = "/ruta/que/no/existe", st_env = "villa_env")
        active.execute()

        assert "Ruta No Encontrada" in capsys.readouterr().out

    def test_mapper_more(self, capsys):
        """ Prueba Uniataria Mapeador - Ruta valida """
        active = Mapper(st_path = "villapy_lib", st_env = "villa_env")
        active.execute()

        assert not "Ruta No Encontrada" in capsys.readouterr().out

# Finite Incantatem
