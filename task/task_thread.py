import threading
from task import automator

def make_thread_task(id_val, pw_val):
    task_thread = threading.Thread(target=automator.start_task, args=(id_val, pw_val), daemon=False)
    task_thread.start()
