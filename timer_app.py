from time import sleep
import subprocess

def timer_task(timer, app):

    subprocess.run(["python3", app])
    sleep(timer * 60)

while True:
    timer_task(0.1, "test.py")