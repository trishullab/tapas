import subprocess
import sys

def eval_program(prog : str, input_data : str, expected_output : str) -> bool:
    actual_output = subprocess.run(
        [sys.executable, "-c", prog], 
        input=input_data.encode('utf-8'), 
        capture_output=True
    ).stdout.decode('utf-8')
    
#     print(f'''
# actual_output: {actual_output}|
# expected_output: {expected_output}|
#     ''')

    return actual_output.strip() == expected_output.strip()