from setuptools import setup

setup(name='formfiller',
      version='0.2',
      description='Create images of filled-out forms',
      url='http://github.com/BlueprintKansas/form-filler-py',
      author='Peter Karman',
      author_email='peter@peknet.com',
      license='MIT',
      packages=['formfiller'],
      zip_safe=False,
      install_requires=['Wand'])

