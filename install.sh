#!/bin/sh

set -e

python=python
pip=pip

# if [ -x "$(command -v apt-get)" ]; then
# 	apt-get install -y $python-dev $python-pip
# 	apt-get install -y $python-pyaudio build-essential swig git libpulse-dev libasound2-dev espeak
# elif [ -x "$(command -v brew)" ]; then
# 	brew install python portaudio swig
# else
# 	echo "Error: Unable to install required dependencies, see: https://github.com/Uberi/speech_recognition for more help." >&2
# 	exit 1
# fi

# $pip install wheel
# $pip install -r requirements.txt

sr_lib=$($python -c "import speech_recognition as sr, os.path as p; print(p.dirname(sr.__file__))")
dest_dir="${sr_lib}/pocketsphinx-data/"

cp -r models/* "${dest_dir}"
chmod -R a+r "${dest_dir}"
