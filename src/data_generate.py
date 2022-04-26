from lib import python_analysis_system as pals
from lib import data_system

if __name__ == "__main__":

    # typeshed_inher_aux : pals.InherAux = pals.make_InherAux()
    typeshed_inher_aux : pals.InherAux = pals.analyze_typeshed(1)
    data_system.generate_dir(typeshed_inher_aux, 'mbpp')

    # data_system.generate_dir('apps')
    # data_system.generate_dir('py150_train')
    # data_system.generate_dir('py150_test')
    # data_system.generate_dir('py150_validation')

    # data_system.generate_dir('cubert')