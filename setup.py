from distutils.core import setup

setup(
    name='socialwealth-redistributor',
    version='0.1',
    packages=['sr'],
    url='https://github.com/przemokraw/socialwealth-redistributor',
    install_requires=[
        'mpmath>=1.0.0',
        'numpy>=1.13.3',
        'prettytable>=0.7.2',
        'scipy>=1.0.0',
        'sympy>=1.1.1'
    ],
    license='',
    author='Przemysław Krawczyk',
    author_email='przemekkraw@gmail.com',
    description=''
)
