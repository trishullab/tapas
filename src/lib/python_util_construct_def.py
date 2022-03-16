from __future__ import annotations

from lib import construct_def
from lib.construct_def import Constructor, Field


singles = [
    Constructor("Declaration", [
        Field("initialized", "bool")
    ]),

    Constructor("Inher", [
        # FUTURE WORK: figure out how to deal with mutually recursive defitions for classes and functions
        # class constructor maps to its type, where type is parameters to class signature (e.g. name * fields * parents) 
        Field("global_env", "PMap[str, Declaration]"),
        Field("nonlocal_env", "PMap[str, Declaration]"),
        Field("local_env", "PMap[str, Declaration]"),
        Field("module_env", "PMap[str, str]"),
        Field("mode", "mode")
    ])

]

choices = {
    "mode" : [

        Constructor(
            "ModuleMode",
            []
        ),

        Constructor(
            "FunctionMode",
            []
        ),

        Constructor(
            "ClassMode",
            []
        ),

        Constructor(
            "NameTargetMode",
            []
        ),

        Constructor(
            "PatternTargetMode",
            []
        ),

        Constructor(
            "SourceMode",
            []
        ),

        Constructor(
            "OpenMode",
            []
        ),

        Constructor(
            "ImportMode",
            [
                Field("context", "str")
            ]
        ),

        Constructor(
            "AttributeMode",
            []
        ),

        Constructor(
            "DeleteMode",
            []
        ),

        Constructor(
            "DeleteSliceMode",
            []
        ),
    ],

    "synth" : [

        Constructor(
            "NoSynth",
            []
        ),

        Constructor(
            "LocalEnvSynth",
            [
                Field("subtractions", "PSet[str]"),
                Field("additions", "PMap[str, Declaration]")
            ]
        ),

        Constructor(
            "DeleteSynth",
            [
                Field("names", "PSet[str]"),
            ]
        ),

        Constructor(
            "SourceSynth",
            [
                Field("declarations", "PMap[str, Declaration]"),
                Field("used_names", "PSet[str]"),
                Field("tokens", "tuple[abstract_token, ...]")
            ]
        ),

        Constructor(
            "TargetSynth",
            [
                Field("names", "PSet[str]"),
                Field("tokens", "tuple[abstract_token, ...]")
            ]
        ),

        Constructor(
            "MultiTargetSynth",
            [
                Field("names", "PSet[str]"),
                Field("tokens", "PSet[tuple[abstract_token, ...]]")
            ]
        ),

        Constructor(
            "OpenSynth",
            [
                Field("path", "str")
            ]
        ),

        Constructor(
            "ImportSynth",
            [
                Field("path", "str")
            ]
        ),

    ]

}


nl = '\n'
def generate_content():
    return (f"""
{construct_def.header}

from pyrsistent.typing import PMap, PSet
from lib.abstract_token import abstract_token 

{f'{nl}{nl}'.join([
    construct_def.generate_single(constructor)
    for constructor in singles 
])}

{f'{nl}{nl}'.join([
    construct_def.generate_choice(type_name, constructors)
    for type_name, constructors in choices.items()
])}
    """)



