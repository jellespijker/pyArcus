import os
import sys
# import pyArcus
def main():
    for k, v in os.environ.items():
        if "PATH" in k:
            print(f"{k} = {os.environ[k]}")

if __name__ == "__main__":
    main()