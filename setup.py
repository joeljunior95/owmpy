from setuptools import find_packages, setup

setup(
    name='owmpy',
    packages=find_packages(include=['owmpy']),
    version='0.1.0',
    description='Python SDK to use the OpenWeatherMap API',
    author='Joel Souza',
    install_requires=[
        'certifi==2024.2.2',
        'charset-normalizer==3.3.2',
        'idna==3.7',
        'python-dateutil==2.9.0.post0',
        'requests==2.31.0',
        'six==1.16.0',
        'urllib3==2.2.1',
        'pytest==8.2.0',
        'pytest-runner==6.0.1',
        'wheel==0.43.0',
        'twine==5.0.0',
        'python-dotenv==1.0.1'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==8.2.0'],
    test_suite='tests',
)