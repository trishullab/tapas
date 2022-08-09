import subprocess
import sys
from typing import Any

from datasets import load_dataset, Dataset
import json

import signal
from typing import Iterable, Union

def run_program(prog : str, input_data : str) -> tuple[str, str]:
    result = subprocess.run(
        [sys.executable, "-c", prog], 
        input=input_data.encode('utf-8'), 
        capture_output=True
    )
    return (result.stdout.decode('utf-8'), result.stderr.decode('utf-8'))
    

def eval_program(prog : str, input_data : str, expected_output : str) -> bool:
    actual_output, _ = run_program(prog, input_data)
    return actual_output.strip() == expected_output.strip()


def get_good_solution(problem, def_count : int) -> Union[str, None]:
    try:
        io_record = json.loads(problem['input_output'])
        inputs = io_record['inputs']
        outputs = io_record['outputs']
        solutions = json.loads(problem['solutions'])


        def_count_solutions = (
            solution
            for solution in solutions
            if solution.strip()
            if solution.count("def ") > def_count
        )


        first_solution = next((
            solution
            for solution in def_count_solutions
            if all(
                not bool(err.strip()) and actual_output.strip() == output.strip()
                for index, raw_input in enumerate(inputs)
                for input in [
                    raw_input 
                    if isinstance(raw_input, str) else 
                    "\n".join(raw_input) 
                    if isinstance(raw_input, list) else
                    str(raw_input)
                ]
                for actual_output, err in [run_program(solution, input)]
                for raw_output in [outputs[index]]
                for output in [
                    raw_output 
                    if isinstance(raw_output, str) else 
                    "\n".join(raw_output) 
                    if isinstance(raw_output, list) else
                    str(raw_output)
                ]
            )
        ), None)

        return first_solution
    except:
        return None


def get_good_apps_data(def_count = -1) -> Iterable[dict[str, str]]:
    ds = load_dataset("codeparrot/apps", split="test")
    assert isinstance(ds, Dataset)
    return ( 
        {
            'id' : problem['problem_id'],
            'solution' : good_solution 
        }
        for problem in ds
        if isinstance(problem, dict)
        for good_solution in [get_good_solution(problem, def_count)]
        if good_solution != None
    )

def add_good_solution(problem, solution):
    problem['good_solution'] = solution
    return problem

def filter_apps_data(def_count = -1):
    ds = load_dataset("codeparrot/apps", split="test")
    assert isinstance(ds, Dataset)
    # ds = ds.filter(lambda example, idx: idx <30, with_indices=True)
    # ds = ds.filter(lambda example, idx: idx > 2672 and idx < 2687, with_indices=True)

    return ds.map(lambda problem : 
        add_good_solution(
            problem, 
            get_good_solution(problem, def_count) or ''
        )
    ).filter(
        lambda problem : problem['good_solution'] != '' 
    )