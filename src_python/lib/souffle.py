import pathlib
import os

import subprocess
from subprocess import TimeoutExpired, PIPE, STDOUT

from lib.instance import instance, match_instance, InstanceHandlers

base_path = pathlib.Path(__file__).parent.absolute()


def from_sequence(instances : list[instance]) -> str:
    acc = "nil" 
    for inst in reversed(instances):
        item = match_instance(inst, InstanceHandlers[str](
            case_Grammar=lambda o : f'$Grammar("{o.options}","{o.selection}")',
            case_Vocab=lambda o : f'$Vocab("{o.options}","{o.selection}")'
        ))
        acc = f'[{item}, {acc}]'
    return acc


def call(souffle_file : str, souffle_input : str) -> str:
    src_souffle_path = os.path.join(base_path, f"../../src_souffle/{souffle_file}")
    proc = subprocess.Popen(["souffle", src_souffle_path], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    outs, err = proc.communicate(souffle_input.encode("utf-8"), timeout=15)
    return outs.decode("utf-8")