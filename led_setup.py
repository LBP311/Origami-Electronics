from setuptools import setup

setup(name='led',
	version='1.0',
	description='LED Sequin Library',
	author='Luis Pizarro',
	author_email='lbp311@nyu.edu'
	url='https://github.com/LBP311/Origami-Electronics/',
	pymodules=['led', 'RPi.GPIO', 'pigpio'],
	)

