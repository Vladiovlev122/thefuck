import os
from thefuck.shells import shell


def match(command):
    return ('permission denied' in command.output.lower()
            and os.path.exists(os.path.expanduser(command.script_parts[0]))
            and not os.access(os.path.expanduser(command.script_parts[0]), os.X_OK))


def get_new_command(command):
    return shell.and_(
        'chmod +x {}'.format(command.script_parts[0][2:]),
        command.script)
