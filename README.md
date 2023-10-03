![Logo](logo.jpg)

# pyEffects  

<!-- Pytest Coverage Comment:Begin -->
\n<!-- Pytest Coverage Comment:End -->
[![PyPI version](https://badge.fury.io/py/pyeffects.svg)](https://badge.fury.io/py/pyeffects) [![Documentation Status](https://readthedocs.org/projects/pyeffects/badge/?version=latest)](https://pyeffects.readthedocs.io/en/latest/?badge=latest)
 [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/vickumar1981/pyeffects/blob/master/LICENSE)

Monads for Python.  Side-effect explicitly.

Handle your side-effects in Python like a boss.  Implements functional types for Either, Option, Try, and Future.

For more detailed information, please refer to the [API Documentation](https://pyeffects.readthedocs.io/en/latest/ "API Documentation").

---
### 1. Install

`pip install pyeffects`

---
### 2. Using Option
```python
>>> from pyeffects.Option import *
>>> val = Some(5).map(lambda v: v * v)
>>> val
Some(25)
>>> val.is_defined()
True
>>> val.get()
25

```

---
### 3. Using Try
```python
>>> from pyeffects.Try import *
>>> val = Success(5).map(lambda v: v * v)
>>> val
Success(25)
>>> val.is_success()
True
>>> val.get()
25

```

---
### 4. Using Either
```python
>>> from pyeffects.Either import *
>>> val = Right(5).map(lambda v: v * v)
>>> val
Right(25)
>>> val.is_right()
True
>>> val.right()
25
```

---
### 5. Using Future
```python
>>> from pyeffects.Future import *
>>> val = Future.of(5).map(lambda v: v * v)
>>> val
Future(Success(25))
>>> val.on_complete(lambda v: print(v))
Success(25)
>>> val.get()
25
```

---
### 6. Reporting an Issue

Please report any issues or bugs to the [Github issues page](https://github.com/vickumar1981/pyeffects/issues). 

---
### 7. License

This project is licensed under the [Apache 2 License](https://github.com/vickumar1981/pyeffects/blob/master/LICENSE).
