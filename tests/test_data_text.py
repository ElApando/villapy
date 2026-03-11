""" Prueba Unitaria Limpieza de texto
python -m tests.test_data_text
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from villapy.data.text import TextManage

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


# activo = TestDataText()
# print(activo.test_caracters_clean())

# Finite Incantatem
