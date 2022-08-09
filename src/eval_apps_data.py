import json
from datasets import load_dataset, Dataset

from subprocess import run
from tapas_lib import io_eval
import shlex

import signal

def check():
    print(io_eval.run_program('''
    ''', f""))


def eval_apps_data():
    ds = load_dataset("codeparrot/apps", split="test")

    error_list = [3785]

    assert isinstance(ds, Dataset)
    for count, problem in enumerate(ds):
        # if count > 1: break
        assert isinstance(problem, dict)
        id = int(problem['problem_id'])
        if id not in error_list: continue


        io_record = json.loads(problem['input_output'])
        inputs = io_record['inputs']
        outputs = io_record['outputs']
        solutions = json.loads(problem['solutions'])

        total = 0
        pass_count = 0
        errors = 0
        
        for solution in solutions:
            for index, input in enumerate(inputs):
                # if index > 3: break
                output = outputs[index]
                try:

                    def handle_signal(signum, frame):
                        raise Exception("TIMEOUT")
                    signal.signal(signal.SIGALRM, handle_signal)
                    signal.alarm(3)
                    actual_output, err = io_eval.run_program(solution, input)
                    passed = actual_output.strip() == output.strip()

                    if not passed:
                        print(f"----------------------")
                        print(f"---#{id}---")
                        print(f"")
                        print(f"::: program  :::") 
                        print(solution)
                        print(f"")
                        print(f"::: input :::")
                        print(f"{input}")
                        print(f"---#{id}---")
                        print(f"")
                        print(f"::: actual_output  :::")
                        print(f"{actual_output.strip()}")
                        print(f"")
                        print(f"::: expected_output  :::")
                        print(f"{output.strip()}")
                        print(f"")
                        print(f"::: err :::")
                        print(err)
                        print(f"---#{id}---")
                        raise Exception()


                    pass_count += (1 if passed else 0)

                    total += 1
                except:
                    errors += 1
                    exit(0)


        print(f'''
passed: {pass_count}/{total}
errors: {errors}
        ''')
if __name__ == "__main__":
    count = 0
    # print(len(io_eval.filter_apps_data(6)))
    for problem in io_eval.filter_apps_data(6):
        assert isinstance(problem, dict)
        print("^^^^^^^^^")
        print(problem.keys())
        print("##")
        print(problem['problem_id'])
        print("<<>>")
        print(json.loads(problem['input_output'])['inputs'])
        print("--")
        print(problem['good_solution'])
        count+= 1
        if count > 4: break
    pass