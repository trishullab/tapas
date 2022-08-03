import subprocess
import sys

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