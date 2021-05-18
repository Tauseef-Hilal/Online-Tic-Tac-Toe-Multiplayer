import os
import sys
import time

try:
    with open('Requirements.txt') as _file:
        deps = _file.readlines()

        for dep in deps:
            print(f"Installing {dep[:-1]}")
            if os.name == "nt":
                os.system(f"py -m pip install {dep[:-1]} -q")
            else:
                os.system(f"pip3 install {dep[:-1]} -q")

except FileNotFoundError:
    print("[ERROR] Requirements.txt not found")
    sys.exit(time.sleep(1))

else:
    print("Installation Successful!")
    sys.exit(time.sleep(1))
