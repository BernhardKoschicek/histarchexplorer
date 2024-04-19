#!/bin/bash

pybabel extract -F translations/babel.cfg -k lazy_gettext -o translations/messages.pot .
#babel init -i translations/messages.pot -d translations -l de
pybabel compile -d translations
pybabel update -i translations/messages.pot -d translations/

