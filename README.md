## Machine Learning Visualization Tools

A single Python file with some tools for visualizing machine learning in the terminal.

![](https://s3.gifyu.com/images/full6615581dfdbfedcb.gif)

This demo is composed of three separate utilities, which are explained below.
Here's how to get started:

```
git clone https://github.com/bwasti/mlvt.git
cd mlvt
python3 -m pip install -r requirements.txt
python3 test.py # demo above
````

or just copy the `mlvt.py` file!

## mlvt.Reprint

`Reprint` helps with in-line animations.
It works by keeping track of how much it printed so far and reprinting it when `flush()` is called.

You can use the `with` statement to hijack `print` statements and `auto_flush=True` to avoid calling `flush()`
in a loop, like so:

```
print("loading!")
with mlvt.Reprint(auto_flush=True) as rp:
  for i in range(100):
    print(f"{i+1}%") # Reprint detects the loop and overwrites in-place
    time.sleep(0.02)
print("done!")
```

![reprint.gif](https://s3.gifyu.com/images/reprint.gif)

or, if you'd prefer to avoid contexts, loop-detection and hijacked builtins
```
print("loading!")
rp = mlvt.Reprint()
for i in range(100):
  rp.print(f"{i+1}%")
  rp.flush()
  time.sleep(0.02)
print("done!")
```

## mlvt.horiz_concat

`horiz_concat` concatenates multi-line strings horizontally, accounting for padding and ANSI escape sequences
(for color text).

```
a = """
{ hello! }
          \_    
"""
b = """
 ___
|. .|
| ^ |
| o |
"""
print(mlvt.horiz_concat(a, b, padding=2))
```

yields

```

               ___
{ hello! }    |. .|
          \_  | ^ |
              | o |
              
```

## `plotille` wrappers

Finally, there are a couple of small [`plotille`](https://pypi.org/project/plotille/) wrappers
that decouple updating charts and printing them.
That library is great on its own, so I encourage you to check it out!

```
import mlvt
import numpy as np

# all charts take in width, height, color
hist = mlvt.Histogram(32, 8, color="bright_blue")
hist.update(np.random.randn(100))
print(hist)
```

gives us

```
 (Counts)  ^
8.80000000 |
7.70000000 | ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
6.60000000 | ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
5.50000000 | ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
4.40000000 | ⠀⠀⠀⠀⠀⠀⠀⠀⢰⣶⣶⠀⠀⢸⡇⣿⠀⢰⣶⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
3.30000000 | ⠀⠀⠀⠀⠀⠀⠀⣿⢸⣿⣿⣿⣿⢸⣿⣿⣿⢸⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
2.20000000 | ⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⠀⠀⠀⢸⡇⠀⠀
1.10000000 | ⠀⠀⢀⣀⡀⣿⣀⣿⣿⣿⣿⣿⣿⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣇⣸⡇⠀⠀
         0 | ⠀⠀⢸⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⡇⠀⠀
-----------|-|---------|---------|---------|-> (X)
           | -2.124059 -0.741902 0.6402548 2.0224115
```
