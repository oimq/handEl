from setuptools import setup, find_packages

setup(name='handEl',
      version=2.0,
      author='oimq',
      url='https://github.com/oimq/handEl',
      author_email='taep0q@gmail.com',
      description='JSON format handler with json module',
      packages=find_packages(),
      install_requires=['elasticsearch', 'tqdm'],
      zip_safe=False
      )