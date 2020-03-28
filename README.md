![Logo](logo.jpg)

# pyEffects  

Monads for Python.  Side-effect explicitly.

Handle your side-effects in Python like a boss.  Implements functional types for Either, Option, Try, and Future.

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
>>> val.get()
25
```

---
### 5. Using Future
```python
>>> from pyeffects.Future import *
>>> val = Future.of(5).map(lambda v: v * v)
>>> val
Future(Success(25))
>>> val.subscribe(lambda v: print(v))
Success(25)
>>> val.get().get()
25
```

---
### 6. Reporting an Issue

Please report any issues or bugs to the [Github issues page](https://github.com/vickumar1981/pyeffects/issues). 

---
### 8. License

This project is licensed under the [Apache 2 License](LICENSE.md).