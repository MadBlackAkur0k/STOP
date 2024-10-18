import psutil
import time

def record_performance(start_time, performance_text):
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Получение информации о текущем процессе
    process = psutil.Process()

    # Получение данных о памяти и CPU для текущего процесса
    memory_info = process.memory_info()
    memory_used = memory_info.rss / (1024 ** 2)  # в МБ (rss - Resident Set Size)
    
    cpu_usage = process.cpu_percent(interval=None)

    # Получение данных об I/O для текущего процесса
    io_counters = process.io_counters()
    io_read = io_counters.read_bytes / (1024 ** 2)  # в МБ
    io_write = io_counters.write_bytes / (1024 ** 2)  # в МБ

    # Запись результатов в текстовое поле
    performance_text.delete(1.0, "end")
    performance_text.insert("end", f"Время выполнения: {elapsed_time:.4f} секунд\n")
    performance_text.insert("end", f"Использование CPU: {cpu_usage}%\n")
    performance_text.insert("end", f"Использование памяти: {memory_used:.2f} МБ\n")
    performance_text.insert("end", f"I/O чтение: {io_read:.2f} МБ\n")
    performance_text.insert("end", f"I/O запись: {io_write:.2f} МБ\n")
