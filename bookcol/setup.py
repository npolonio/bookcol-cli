from setuptools import setup, find_packages

setup(
    name='bookcol',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click>=8.0.0',
        'inquirer>=2.7.0',
    ],
    entry_points={
        'console_scripts': [
            'bookcol = bookcol.__main__:menu',
        ],
    },
)
