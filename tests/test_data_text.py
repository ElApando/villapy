""" Prueba Unitaria Limpieza de texto
python -m tests.test_data_text
"""

import sys
from pathlib import Path

import bcrypt

sys.path.append(str(Path(__file__).resolve().parents[1]))

from villapy_lib.data.text import TextManage

class TestDataText:
    """DCO"""

    def test_caracters_clean(self):
        """ Docstring for test_caracters_clean
        """
        active = TextManage()
        st_prove = active.caracters_clean("JuanÑd´%>")
        assert st_prove == "JuanÑd"

    def test_accent_clean(self):
        """
        Docstring for test_accent_clean
        """
        active = TextManage()
        st_prove = active.accent_clean("Júán Sébástían")
        assert st_prove == "Juan Sebastian"

    def test_save_numbers(self):
        """
        Docstring for test_save_numbers
        """
        active = TextManage()
        assert active.save_numbers("09.45t") == "09.45"
        assert active.save_numbers("-09.45t") == "-09.45"

    def test_modify_date(self):
        """
        Docstring for test_modify_date
        """
        active = TextManage()
        assert active.modify_date("09/03/2026") == "2026-03-09"
        assert active.modify_date("09-03-2026") == "2026-03-09"
        assert active.modify_date("09.03.2026") == "2026-03-09"
        assert active.modify_date("09/25/2026") == "2026-09-25"
        assert active.modify_date("2026-09-03") == "2026-09-03"
        assert active.modify_date("2026-03-29") == "2026-03-29"

    def test_valid_name(self):
        """
        Docstring for test_modify_date
        """
        active = TextManage()
        assert active.valid_name("Juan")
        assert not active.valid_name("Juan2")

    def test_valid_email(self):
        """
        Docstring for test_modify_date
        """
        active = TextManage()
        assert active.valid_email("Juan.rodrigo@hotmial.com")
        assert not active.valid_email("..juan_albero@gmail.com")

    def test_valid_phone(self):
        """
        Docstring for test_modify_date
        """
        active = TextManage()
        assert active.valid_phone("5578936521")
        assert not active.valid_phone("0123456789")
        assert active.valid_phone("2345678910")
        assert not active.valid_phone("0123456ty9")

    def test_change_word(self):
        """
        Docstring for test_modify_date
        """
        active = TextManage()
        st_text = "A"
        di_example = {"A" : "a"}
        assert active.change_word(st_text, di_example) == "a"

    def test_hash_password(self):
        """
        Docstring for test_modify_date
        """
        active = TextManage()
        st_password = "Juan".encode("utf-8")
        st_hash = active.hash_password("Juan").encode("utf-8")
        # assert active.hash_password("Juan") == "2026-03-09"
        assert bcrypt.checkpw(st_password, st_hash)


# activo = TestDataText()
# print(activo.test_caracters_clean())

# Finite Incantatem
