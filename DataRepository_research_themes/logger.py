import sys
from os.path import join

import logging
formatter = logging.Formatter('%(levelname)s: %(message)s')


class LogClass:

    def __init__(self, log_dir, logfile):
        self.LOG_FILENAME = join(log_dir, logfile)
        self._log = self._get_logger()

    def _get_logger(self):
        log_level = logging.INFO
        log = logging.getLogger(self.LOG_FILENAME)
        if not getattr(log, 'handler_set', None):
            log.setLevel(logging.INFO)
            sh = logging.StreamHandler(sys.stdout)
            sh.setFormatter(formatter)
            log.addHandler(sh)

            fh = logging.FileHandler(self.LOG_FILENAME)
            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)
            log.addHandler(fh)

            log.setLevel(log_level)
            log.handler_set = True
        return log
