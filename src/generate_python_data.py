from lib import python_aux_system as pals
from lib import python_data_system

if __name__ == "__main__":

    package = pals.analyze_typeshed()
    python_data_system.generate_dir(package, 'mbpp')

    # data_system.generate_dir(package, 'apps')
    # data_system.generate_dir(package, 'py150_train')
    # data_system.generate_dir(package, 'py150_test')
    # data_system.generate_dir(package, 'py150_validation')

    # data_system.generate_dir(package, 'cubert')