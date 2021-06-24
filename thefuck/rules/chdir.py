import re
from thefuck.utils import for_app
from thefuck.specific.sudo import sudo_support
from thefuck.shells import shell


@sudo_support
@for_app('chdir')
def match(command):
    return (
        command.script.startswith('chdir') and any((
            'cannot find the path' in command.output.lower(),
            'cannot find path' in command.output.lower(),
            'can\'t cd to' in command.output.lower()
        )))


@sudo_support
def get_new_command(command):
    shell_name = shell.info()
    if shell_name == 'pwsh' or shell_name == 'powershell':
        new_command = ('mkdir -p \\1' + '; chdir\\1')
        return re.sub(r'^chdir(.*)', new_command, command.script)
    else:
        repl = ('mkdir -p \\1; chdir \\1')
        return re.sub(r'^chdir(.*)', repl, command.script)
