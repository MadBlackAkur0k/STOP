import logging

def setup_logging():
    loggers = {
        'show_tables': create_logger('show_tables.log'),
        'show_structure': create_logger('show_structure.log'),
        'show_data': create_logger('show_data.log'),
        'insert_data': create_logger('insert_data.log'),
        'delete_records': create_logger('delete_records.log'),
        'update_records': create_logger('update_records.log')
    }
    return loggers

def create_logger(filename):
    logger = logging.getLogger(filename)
    handler = logging.FileHandler(filename)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
