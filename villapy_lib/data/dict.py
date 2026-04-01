""" DOC """

from typing import Dict, List, Any, Union

class DictManage:
    """ DOC"""

    def __init__(self):
        """ DOC """
        pass

    def dict_comparation(self, di_1: Union[Dict[Any, Any], List[Any], str, int],
                         di_2: Union[Dict[Any, Any], List[Any], str, int],
                         ls_save: List[Any], st_path: str = ""):
        """ Compración de diccionarios

        La funcion toma dos diccionariso de la misma estructura y compara los cambios, esto con la
        finalidad de ubicar cambios en ellos.

        Parameters:
            di_1 (Dict): Diccionario anterior
            di_2 (Dict): Diccionario actual
            ls_save (List): Lista para almacenar los faltantes
            st_path (str): Cadena de texto que guarda la ruta explorada, funciona para el debug

        Returns:
            ls_save (List): De vuelve la lista con los items nuevos en el diccionario de hoy
        """

        if isinstance(di_1, dict) and isinstance(di_2, dict):
            keys = set(di_1.keys()) | set(di_2.keys())

            for jj in keys:
                new_path = f"{st_path}.{jj}" if st_path else jj

                if isinstance(di_1, dict) and isinstance(di_2, dict): # type:ignore
                    compare = list(set(di_2.keys())-set(di_1.keys()))

                    if compare:
                        if not compare in ls_save:
                            ls_save.append(compare)

                        continue

                self.dict_comparation(di_1[jj], di_2[jj], ls_save, new_path)

        return ls_save

# Finite Incantatem
