
from setuptools import setup, find_packages

setup(
    name='ipymarkup',
    version='0.1.0',
    description='NER markup visualisation for Jupyter Notebook',
    url='https://github.com/natasha/ipymarkup',
    author='Alexander Kukushkin',
    author_email='alex@alexkuk.ru',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='ner, markup, jupyter, ipython',
    packages=find_packages(),
    install_requires=[
        'intervaltree==2.1.0'
    ]
)
