from setuptools import setup , find_packages

with open("requirements.txt") as f :
    requirements = f.read().splitlines()


setup(
    name="mlops-salary-prediction" , 
    version="0.1",
    author="mahmoud tolba" ,
    packages=find_packages(requirements) , 
    install_requires=requirements
)