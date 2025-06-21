import threading
from task import automator

def make_thread_task():
    task_thread = threading.Thread(target=automator.start_task, daemon=False)
    task_thread.start()
