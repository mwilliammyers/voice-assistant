from __future__ import print_function, unicode_literals

import json
import readline
from builtins import input, str

from main import action_from
from snips_nlu import SnipsNLUEngine

nlu_engine = SnipsNLUEngine().from_path("models/nlu/engine")

try:
    while True:
        text = str(input("> "))
        parsed = nlu_engine.parse(text)
        print(json.dumps(parsed, indent=4))
        action_from(**parsed)()
except (KeyboardInterrupt, EOFError):
    pass
