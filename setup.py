from setuptools import setup , find_packages

with open("requiremenst.txt") as f :
    requirements = f.read().splitlines()


setup(
    name="mlops-project-hotel-reservation" , 
    version="0.1",
    author="mahmoud tolba" ,
    packages=find_packages(requirements) , 
    install_requires=requirements
)