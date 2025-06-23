import threading
from task import automator
from data import button_data

def make_thread_task():
    enable_execute_button()
    task_thread = threading.Thread(target=automator.start_task, daemon=False)
    task_thread.start()

def enable_execute_button():
    buttons = button_data.ButtonData()
    buttons.execute_button_Enable(False)
