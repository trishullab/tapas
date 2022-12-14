from distutils.file_util import write_file
from typing import Iterable
from tapas_lib import python_aux_system as pals
from tapas_lib import python_data_system
from pyrsistent import pset, m, pmap
from pyrsistent.typing import PMap
from tapas_lib import python_data_system

import json
from datasets import load_dataset, Dataset, concatenate_datasets
from datasets import load_from_disk

from tapas_base.util_system import write, project_path

from tapas_lib import generic_tree_system
from tapas_lib import python_ast_system 

from tapas_base import abstract_token_system as ats


def merge_count_map(a_map : PMap[str, int], b_map : PMap[str, int]) -> PMap[str, int]:
    return a_map + pmap({
        k : (
            c + a_map[k]
            if a_map.get(k) else
            c
        )
        for k, c in b_map.items()
    })


if __name__ == "__main__":

    package = pals.analyze_typeshed_cache()


    processed_fname = 'filtered_main_def_count_and_line_count_def_min_count_3_def_max_count_10'



    ds = load_from_disk(project_path(f"tapas_res/sanity_check/{processed_fname}"))
    assert isinstance(ds, Dataset)

    abstract_data_dirpath = project_path(f"tapas_res/sanity_check/token_data")

    def write_split(ds : Dataset, name, package : PMap[str, pals.ModulePackage]):
        count_map = m()
        for problem in ds:
            assert isinstance(problem, dict)
            i = problem['problem_id']
            file_name = f'{name}_{str(i).zfill(5)}.jsonl'
            solution = problem['good_solution']
            data = [
                lambda:python_data_system.add_semantic_data(python_ast_system.serialize(python_ast_system.parse(solution)), package)
            ]
            new_count_map = python_data_system.write_data(abstract_data_dirpath, file_name, data)
            count_map = merge_count_map(count_map, new_count_map)
        return count_map

    count_map = write_split(ds, "sanity", package)

    write(abstract_data_dirpath, f'z_stats.json', json.dumps({k:v for k, v in count_map.items()}))
