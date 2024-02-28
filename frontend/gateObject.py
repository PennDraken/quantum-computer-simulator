
# hello world function
import os

cmd = 'wmic desktopmonitor get screenheight, screenwidth'
(x,y) = tuple(map(int, os.popen(cmd).read().split()[-2::]))
print(y)

def helloWorld():
    print("Hello World!")

    