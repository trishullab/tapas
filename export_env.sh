#!/bin/bash

conda env export --no-builds | grep -v "prefix:" | grep -v "name:" > environment.yml