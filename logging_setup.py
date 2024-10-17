import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

insert_logger = logging.getLogger("insert_logger")
insert_handler = logging.FileHandler("insert.log")
insert_handler.setLevel(logging.INFO)
insert_logger.addHandler(insert_handler)

update_logger = logging.getLogger("update_logger")
update_handler = logging.FileHandler("update.log")
update_handler.setLevel(logging.INFO)
update_logger.addHandler(update_handler)

delete_logger = logging.getLogger("delete_logger")
delete_handler = logging.FileHandler("delete.log")
delete_handler.setLevel(logging.INFO)
delete_logger.addHandler(delete_handler)

select_logger = logging.getLogger("select_logger")
select_handler = logging.FileHandler("select.log")
select_handler.setLevel(logging.INFO)
select_logger.addHandler(select_handler)
