from setuptools import find_packages, setup

setup(
    name='chemprop_solvation',
    version='0.0.2',
    packages=find_packages(),
    package_data={"":["final_models/*/*/*/model.pt"]},
    url='https://github.com/fhvermei/chemprop_solvation',
    author='fhvermei',
    author_email='',
    license='MIT',
)
