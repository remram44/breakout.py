import io
import os
from setuptools import setup


# pip workaround
os.chdir(os.path.abspath(os.path.dirname(__file__)))


with io.open('README.rst', encoding='utf-8') as fp:
    description = fp.read()

setup(name='api_stats',
      version='0.1',
      py_modules=['breakout'],
      description="Drop to debugger when given output is written.",
      author="Remi Rampin",
      author_email='remirampin@gmail.com',
      maintainer="Remi Rampin",
      maintainer_email='remirampin@gmail.com',
      url='https://github.com/remram44/breakout',
      long_description=description,
      license='BSD',
      keywords=['log', 'debug', 'debugger', 'output'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Topic :: Software Development',
          'Topic :: Utilities'])
