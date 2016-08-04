# coding=utf-8
from setuptools import setup

"""
Define Django application settings with Django ORM models and edit them in the admin area.
"""

setup(
	name='django-modelsettings',
	version='0.2.3',
	url='https://github.com/IlyaSemenov/django-modelsettings',
	license='BSD',
	author='Ilya Semenov',
	author_email='ilya@semenov.co',
	description=__doc__,
	long_description=open('README.rst').read(),
	packages=['dbsettings'],
	package_data={"dbsettings": ["templates/dbsettings/*.html"]},
	install_requires=['Django>=1.7'],
	classifiers=[],
)
