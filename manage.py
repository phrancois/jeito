#!/usr/bin/env python3
import os
import sys

activate_this = os.path.join(os.path.dirname(__file__), 'env/bin/activate_this.py')
with open(activate_this) as f:
    code = compile(f.read(), activate_this, 'exec')
    exec(code, dict(__file__=activate_this))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jeito.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
