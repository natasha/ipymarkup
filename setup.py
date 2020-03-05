
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
    install_requires=requirements
)
