from lib import python_aux_system as pals
from lib import python_data_system

if __name__ == "__main__":

    package = pals.analyze_typeshed()
    # python_data_system.generate_dir(package, 'mbpp')

    # python_data_system.generate_dir(package, 'apps')
    # python_data_system.generate_dir(package, 'py150_train')
    # python_data_system.generate_dir(package, 'py150_test')
    # python_data_system.generate_dir(package, 'py150_validation')

    python_data_system.generate_dir(package, 'cubert')