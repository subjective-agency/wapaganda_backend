#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from supaword.log_helper import logger


def custom_command(command_handlers):
    command = sys.argv[1] if len(sys.argv) > 1 else None

    def str_to_bool(s):
        return s.lower() in ("true", "yes", "1")

    if command in command_handlers:
        params_num = len(sys.argv) - 2
        expected_params_num = len(command_handlers[command]["params"])
        if params_num == expected_params_num:
            logger.info(f"Executing command '{command}'")
            params_pack = {command_handlers[command]["params"][i]: sys.argv[i + 2] for i in range(params_num)}
            # Check for boolean flags and convert "true" or "false" to boolean values
            for arg_index in range(2, len(sys.argv)):
                if sys.argv[arg_index] in ["true", "false"]:
                    params_pack[command_handlers[command]["params"][arg_index - 2]] = str_to_bool(sys.argv[arg_index])
            logger.info(f"Parameters: {params_pack}")
            command_handlers[command]["handle"](**params_pack)
            return 0
        else:
            logger.error(f"Invalid number of parameters {params_num} for command '{command}'")
            return 1


def main():
    """
    Run administrative tasks
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supaword.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
