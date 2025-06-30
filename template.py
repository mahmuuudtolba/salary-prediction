import os
from pathlib import Path


list_of_files = [
    "artifacts/raw" ,
    "config/config.yaml" , 
    "config/__init__.py" ,  
    "config/path_config.py" ,  
    "config/model_params.py" ,
    "notebook/notebook.ipynb" , 
    "src/__init__.py",
    "templates/index.html",
    "utils/__init__.py",
    "README.md",
    "requirements.txt",
    "setup.py"

]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir , filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath , "w") as f :
            pass
        print(f"Creating empty file : {filepath}")

    else:
        print(f"{filename} is already exists")