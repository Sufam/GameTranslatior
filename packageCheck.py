import importlib.util, subprocess, sys

def checkPackage(package):
    spec = importlib.util.find_spec(package)
    if spec == None:
        print(f"Miss package {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    else:
        print(f"{package} installed")

packagefile = "./requirements.txt"

with open(packagefile, "r", encoding="utf-8") as package:
    requitrement = package.readlines()

    for i in requitrement:
        checkPackage(i.split("==")[0])
