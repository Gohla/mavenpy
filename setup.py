from setuptools import setup

setup(
  name='mavenpy',
  version='0.1.3',
  description='Wrapper for calling Maven from Python',
  url='http://github.com/Gohla/mavenpy',
  author='Gabriel Konat',
  author_email='gabrielkonat@gmail.com',
  license='Apache 2.0',
  packages=['mavenpy'],
  install_requires=['pystache'],
  test_suite='nose.collector',
  tests_require=['nose']
)
