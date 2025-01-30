import time

def countdown():
    sec = 5

    while sec >= 0:
        print(sec)
        sec -= 1
        time.sleep(1)
    return False

x = countdown()
print(x)