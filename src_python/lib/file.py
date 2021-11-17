import logging
import os

# logging.basicConfig(level=logging.INFO)

def write(dirpath : str, fname : str, code : str, append : bool = False):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    fpath = os.path.join(dirpath, f"{fname}")

    with open(fpath, 'a' if append else 'w') as f:
        # logging.info(f"Writing file: {fpath}")
        f.write(code)