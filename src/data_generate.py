from lib import python_analysis_system as pals
from lib import data_system

if __name__ == "__main__":

    package = pals.analyze_typeshed()
    data_system.generate_dir(package, 'mbpp')

    # data_system.generate_dir('apps')
    # data_system.generate_dir('py150_train')
    # data_system.generate_dir('py150_test')
    # data_system.generate_dir('py150_validation')

    # data_system.generate_dir('cubert')