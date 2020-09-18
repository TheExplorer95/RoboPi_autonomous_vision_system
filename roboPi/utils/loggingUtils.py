import logging

class MainLogger():
    
        __logFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    def __init__(name='root', level=logging.INFO, fileName='ProblemSolver'):
        # create logger
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        # create file handler
        fh = logging.FileHandler(fileName)
        fh.setLevel(level)
    
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)

        formatter = logging.Formatter(logFormat)
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

class SubLogger():
    # creates a submodule for the root logger
    # deeper variable scopes belong to this logger

    def __init__(name):
        self._module_logger = logging.getLogger(name)

