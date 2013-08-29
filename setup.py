# coding=utf-8
from distutils.core import setup

"""
Django application that allows to create user-adjustable application settings
which are stored in database models
"""

setup(
	name='django-modelsettings',
	version='0.1',
	url='https://github.com/IlyaSemenov/django-modelsettings',
	license='BSD',
	author='Ilya Semenov',
	author_email='me@ilyasemenov.com',
	description='django user-adjastable settings',
	long_description=__doc__,
	packages=['django_modelsettings'],
	include_package_data=True,
	zip_safe=False,
	platforms='any',
	install_requires=[],
	classifiers=[
		# As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
		'Framework :: Django',
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Intended Audience :: Information Technology',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Internet',
		'Topic :: Scientific/Engineering',
	]
)
