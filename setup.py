from setuptools import setup, find_namespace_packages

setup(name='clean-folder',
      version='0.0.1',
      description='Sorting files into folders depending on the type of their extension',
      author='Yuliia Manhupli',
      author_email='juliamangup@gmail.com',
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['clean-folder=clean_folder.clean:main']}
)