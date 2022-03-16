if (x := (z := "59293"), False)[-1]:
    print (f"True {x, z}")
else:
    print (f"False {x, z}")

import os


for ooga in (xs := [1, 2, 3]):
    l = 2
    print(xs)
    print(ooga)

print(xs)

def write(dirpath : str, fname : str, code : str, append : bool = False):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    fpath = os.path.join(dirpath, fname)

    with (g := open(fpath, 'a' if append else 'w')) as f:
        f.write(code)

    d = g
    e = f

(y := x, z)