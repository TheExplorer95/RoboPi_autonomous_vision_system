import logging

    
def MainLogger(loggerName='root', level=logging.INFO, fileName='ProblemSolver.log', logFormat='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    # create logger
    logger = logging.getLogger(loggerName)
    logger.setLevel(level)
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

def SubLogger(loggerName):
    # creates a submodule for the root logger
    # deeper variable scopes belong to this logger
    module_logger = logging.getLogger(loggerName)

