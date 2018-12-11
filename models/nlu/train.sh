#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

cd "${DIR}"

rm -rf engine/

snips-nlu generate-dataset en *.yaml > dataset.json
snips-nlu train dataset.json engine
