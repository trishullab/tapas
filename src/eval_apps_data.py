import json
from datasets import load_dataset, Dataset

from subprocess import run
from tapas_lib import io_eval
import shlex

import signal

if __name__ == "__main__":

#     result = apps_mock.eval_program('''
# x = input()
# y = input()
# print(int(x) + int(y))
# ''', '1\n1\n', '2\n')
#     print(result)
#     result = io_eval.eval_program('''
# (x0, y0, A, C, B, D) = list(map(int, input().split()))
# pts = [[x0, y0]]
# for i in range(100):
#     (nx, ny) = [((pts[(- 1)][0] * A) + B), ((pts[(- 1)][1] * C) + D)]
#     pts.append([nx, ny])
#     if max(nx, ny) > (10000000000000000 * 10000000000000000):
#         break
# (x, y, t) = list(map(int, input().split()))
# _max = 0
# for i in range(len(pts)):
#     for j in range(len(pts)):
#         if (((abs((pts[i][0] - pts[j][0])) + abs((pts[i][1] - pts[j][1]))) + abs((x - pts[i][0]))) + abs((y - pts[i][1]))) <= t:
#             _max = max(_max, (abs((i - j)) + 1))
# print(_max)
# ''', '1 1 2 3 1 0\n2 4 20\n', '3')
#     print(result)

    ds = load_dataset("codeparrot/apps", split="test")

    assert isinstance(ds, Dataset)
    for count, problem in enumerate(ds):
        if count > 1: break
        assert isinstance(problem, dict)
        id = problem['problem_id']
        io_record = json.loads(problem['input_output'])
        inputs = io_record['inputs']
        outputs = io_record['outputs']
        solutions = json.loads(problem['solutions'])

        total = 0
        pass_count = 0
        errors = 0
        
        for solution in solutions:
            for index, input in enumerate(inputs):
                if index > 3: break
                output = outputs[index]
                try:

                    def handle_signal(signum, frame):
                        raise Exception("TIMEOUT")
                    signal.signal(signal.SIGALRM, handle_signal)
                    signal.alarm(3)
                    passed = io_eval.eval_program(solution, input, output)
                    pass_count += (1 if passed else 0)

                    total += 1
                except:
                    errors += 1

        print(f'''
passed: {pass_count}/{total}
errors: {errors}
        ''')