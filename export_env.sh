#!/bin/bash

conda env export --from-history --no-builds | grep -v "prefix:" | grep -v "name:" > environment.yml