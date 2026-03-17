"""
Docstring for looging.looging
"""

import datetime

from villapy.config.static import di_config

class WriteLogs:
    """
    Docstring for WriteLogs
    """

    def __init__(self)->None:
        """
        Docstring for __init__
        """
        self.st_origin_path = di_config["base_path"]

    # def check_path(str):

    def logs_with_name(self, st_name_rate: str, st_text: str)->None:
        """Escribe logs registros del proceso en cuestión

        Parameters:
            - st_name_rate *(str)* - nombre del proceso
            - st_text *(str)* - Mensaje que se guarda en los registros
        Returns:
            - None
        """
        st_name = st_name_rate.lower()
        with open(f"{self.st_origin_path}/logs/logs_{st_name}.txt","a",encoding="utf-8") as file:
            st_time = str(datetime.datetime.now())
            file.write(f"\n{st_time} {st_text}")

    def write_logs(self, st_text: str)->None:
        """ Escribe lols registros del proceso en cuestión

        Parameters:
            st_text (str): Mensaje que se guarda en los registros
        """

        with open(f"{self.st_origin_path}/logs/logs_{datetime.datetime.now().date()}.txt", "a",
                encoding="utf-8") as file:
            st_time = str(datetime.datetime.now())
            file.write(f"\n{st_time} {st_text}")



# Finite Incantatem
