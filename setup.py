
from setuptools import setup, find_packages


description = '''
ipymarkup 
=========

NER markup visualisation for Jupyter Notebook. 

::

  from ipymarkup import Span, AsciiMarkup

  text = 'a d a b a a a b c c c f d'
  spans = [
    Span(0, 13, 'a'),
    Span(2, 25, 'd'),
    Span(6, 15, 'b'),
    Span(16, 21, 'c'),
    Span(22, 23, 'f'),
  ]
  AsciiMarkup(text, spans)

  >>> a d a b a a a b c c c f d
  ... a------------ c---- f 
  ... d----------------------
  ... b-------- 


For more examples and explanation see `ipymarkup documentation <http://nbviewer.jupyter.org/github/natasha/ipymarkup/blob/master/docs.ipynb>`_.
'''

setup(
    name='ipymarkup',
    version='0.5.0',
    description='NER markup visualisation for Jupyter Notebook',
    long_description=description,
    long_description_content_type='text/x-rst',
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
