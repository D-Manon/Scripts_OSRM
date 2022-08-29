import time


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and save the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        duree_secondes = time.perf_counter() - self._start_time
        self._start_time = None
        q, s = divmod(duree_secondes, 60)
        h, m = divmod(q, 60)
        duree = "%d heure(s) %d minute(s) %d seconde(s)" % (h, m, s)
        return duree

    def stop_write_close(self, etape, pth_folder_results):
        """Arrête le timer, print et enregistre la durée dans un document texte"""
        duree = self.stop()
        line = f"{etape} : {duree}"
        print(f"Fin étape {line}") 
        line = ['', f"{line} \n"]
        file = open(f'{pth_folder_results}tps_creation_reseau.txt', 'a')
        file.writelines('\n'.join(line))
        file.close()
