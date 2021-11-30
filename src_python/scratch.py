

def split(zs : tuple) -> list[tuple[tuple, tuple]]:
    nil = tuple([])
    snoc = lambda xs, x : xs + tuple([x])
    return (
        [(zs, nil)] + 
        ([(ys, snoc(xs,hd))
          for hd in [zs[-1]]
          for zs_tl in [zs[:-1]]
          for (ys, xs) in split(zs_tl)
         ] if len(zs) > 0 else [])
    ) 


import json
for ys, xs in split((1,2,3,4)):
    print(json.dumps(ys) + "     " + json.dumps(xs)) 