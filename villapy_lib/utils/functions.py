""" DOC """

# pylint: disable=broad-exception-caught

from typing import Callable, Any

import time
import traceback

from villapy_lib.looging.write_log import WriteLogs

class ManageFunctions:
    """ Manejo de Funciones """

    def __init__(self) -> None:
        """ Manejo de Funciones 
        
        Se pueden modificar el tiempo de espera y los intentos máximos.
        
        Las funciones que se manejan son :
        - retry_function
        - run_satge
        """

        self.in_wait_retry = 5
        self.in_max_retry = 3
        self.logs_activate = WriteLogs()

    def retry_function(self, function: Callable[..., None], st_site: str,
                       *args, **kwargs) -> Any: # type: ignore
        """ retry_function
         
        Reintenta la función ingresada con la finalidad de que cumpla con lo enconmendado

        Parameter:
            fuction (def)* Fución que se quiere repetir en caso de fallo
            max_retry (int)* Número máximo de reintentos
            wait (int)* Tiempo entre reintento
            *args (Any)* Argumentos de la fución a evaluar
            **kwargs  (Any)* Argumentos de la fución a evaluar
        """
        for trying in range(0, self.in_max_retry+1, 1):
            try:
                return function(*args, **kwargs)

            except Exception as e:
                error_trace = traceback.format_exc()

                if trying <= self.in_max_retry:
                    self.logs_activate.logs_with_name(
                        st_site, f"Intento {trying} {e}\n{error_trace}")
                    time.sleep(self.in_wait_retry)

                else:
                    self.logs_activate.logs_with_name(st_site, f"Maximo intentos {e}")
                    raise TimeoutError("Se terminaron los intentos")

                return "fail"

    def run_stage(self, st_name_process: str, fu_function: Callable[..., None]) -> None: # No puede ser importado con _
        """ Run Stage
        
        La función registra la actividad de las funciones que se ejecutan. Registra tiempo de
        ejecución, que proceso se ejecuta, y si hubo algun error en la ejecución

        Parameters:
            st_name_process (str): Nombre del proceso que se ejecutará
            fu_function (Callable): Función en cuestión
        """
        fl_start_time = time.time()
        self.logs_activate.write_logs(f"[START] - Proceso {st_name_process}")

        try:
            fu_function()
            fl_duration = time.time() - fl_start_time
            self.logs_activate.write_logs(
            f"[INFO] - Tiempo de ejecución {st_name_process} - {fl_duration:.2f}s")
            self.logs_activate.write_logs(f"[END] - Proceso {st_name_process}")

        except Exception as e:
            self.logs_activate.write_logs(f"[FALLO] - {st_name_process} - Error {e}")
            raise  TimeoutError("Fallo el proceso")

# Finite Incantatem
