#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
<<<<<<< HEAD
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "serce.settings.dev")
=======
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gettingstarted.settings")
>>>>>>> 353f0ebb142065a5637d555813b6efce41e85f92

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
