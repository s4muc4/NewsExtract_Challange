import logging
import uuid

class Log_Message():
    def __init__(self) -> None:
        """Initializing class of logs"""
        logger = logging.getLogger(__name__)
        logger.propagate = True
        execution_id = uuid.uuid4()
        logging.basicConfig(filename='output/myapp.log',
                        level=logging.INFO,
                        format=f'Execution ID: {execution_id} - %(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
        logging.getLogger('Files').setLevel(logging.WARNING)
        logging.getLogger('logger').setLevel(logging.WARNING)
        logging.getLogger('_file').setLevel(logging.WARNING)
        self.logger = logger

    def log_info(self,message):
        """Print message and save in log file with type: info"""
        print("INFO - " + message)
        self.logger.info(message)

    def log_warn(self,message):
        """Print message and save in log file with type: warn"""
        print("WARN - " + message)
        self.logger.warn(message)

    def log_error(self,message):
        """Print message and save in log file with type: error"""
        print("ERROR - " + message)
        self.logger.error(message)

    

        
