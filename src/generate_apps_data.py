from distutils.file_util import write_file
from typing import Iterable
from tapas_lib import python_aux_system as pals
from tapas_lib import python_data_system
from pyrsistent import pset, m, pmap
from pyrsistent.typing import PMap
from tapas_lib import python_data_system

import json
from datasets import load_dataset, Dataset, concatenate_datasets

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

    ds_train = load_dataset("codeparrot/apps", split="train")
    ds_test = load_dataset("codeparrot/apps", split="test")

    assert isinstance(ds_train, Dataset)
    assert isinstance(ds_test, Dataset)

    abstract_data_dirpath = project_path(f"tapas_res/apps")

    def write_split(ds : Dataset, name, package : PMap[str, pals.ModulePackage]):
        count_map = m()
        for problem in ds:
            assert isinstance(problem, dict)
            i = problem['problem_id']
            file_name = f'{name}_{str(i).zfill(5)}.jsonl'
            solutions = json.loads(problem['solutions'])
            abstract_data = [
                python_ast_system.serialize(python_ast_system.parse(solution))
                for solution in solutions
            ]
            new_count_map = python_data_system.write_data(abstract_data_dirpath, file_name, package, abstract_data)
            count_map = merge_count_map(count_map, new_count_map)
        return count_map

    count_map_train = write_split(ds_train, "apps_train", package)
    count_map_test = write_split(ds_test, "apps_test", package)
    count_map = merge_count_map(count_map_train, count_map_test)

    write(abstract_data_dirpath, f'z_stats.json', json.dumps(count_map))
