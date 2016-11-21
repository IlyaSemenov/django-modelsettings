"""Define Django application settings with Django ORM models and edit them in the admin area."""

from setuptools import setup, find_packages

setup(
	name='django-modelsettings',
	version='0.5.0',
	url='https://github.com/IlyaSemenov/django-modelsettings',
	license='BSD',
	author='Ilya Semenov',
	author_email='ilya@semenov.co',
	description=__doc__,
	long_description=open('README.rst').read(),
	packages=find_packages(),
	include_package_data=True,
	install_requires=['Django>=1.7'],
	classifiers=[],
)
