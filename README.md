# ipymarkup [![Build Status](https://travis-ci.org/natasha/ipymarkup.svg?branch=master)](https://travis-ci.org/natasha/ipymarkup)

NER markup visualisation for Jupyter Notebook. 
<img src="table.png"/>

# Install

`ipymarkup` supports both Python 2.7+ / 3.4+, ascii version should work on 2.7+ / 3.3+, PyPy but not tested

```bash
$ pip install ipymarkup
```

# Usage

```python
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

```
```
a d a b a a a b c c c f d
a------------   c---- f  
  d----------------------
      b--------          
```


For more examples and explanation see [ipymarkup documentation](http://nbviewer.jupyter.org/github/natasha/ipymarkup/blob/master/docs.ipynb).

# License

Source code of `ipymarkup` is distributed under MIT license (allows modification and commercial usage)

# Support

- Chat — https://telegram.me/natural_language_processing
- Issues — https://github.com/natasha/ipymarkup/issues
