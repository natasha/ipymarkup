
from setuptools import setup, find_packages


with open('README.md') as file:
    description = file.read()


with open('requirements/main.txt') as file:
    requirements = list(file)


setup(
    name='ipymarkup',
    version='0.5.0',
    description='NER markup visualisation for Jupyter Notebook',
    long_description=description,
    long_description_content_type='text/markdown',
    url='https://github.com/natasha/ipymarkup',
    author='Alexander Kukushkin',
    author_email='alex@alexkuk.ru',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
    keywords='ner, markup, jupyter, ipython',
    packages=find_packages(),
    install_requires=requirements
)
