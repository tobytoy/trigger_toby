import subprocess
from pathlib import Path
import ipywidgets as widgets
from IPython.display import clear_output
from IPython.core.magic import register_line_magic

wid_password = widgets.Password(description='Password')
wid_install_btn = widgets.Button(description='Install', disabled=False)

def install_btn(wid_install_btn):
    wid_password.value
    if not Path('/root/.ssh').exists():
        password_cipher = base64.b64encode(wid_password.value.encode('utf-8')).decode('UTF-8')
        cmd_list = [
            ['unzip', '-P', password_cipher, 'key.zip'],
            ['unzip', '-P', wid_password.value, 'root_keys.zip'],
            ['cp', '-r', 'root_keys/source_ssh/', '/root/.ssh'],
            ['ssh-keyscan github.com >> /root/.ssh/known_hosts'],
            ['chmod', '644', '/root/.ssh/known_hosts'],
            ['chmod', '600', '~/.ssh/id_ed25519'],
            ['git', 'clone', 'git@github.com:tobytoy/administrator_toby.git'],
        ]
        for cmd in cmd_list:
            if len(cmd) > 1:
                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
            else:
                subprocess.run(cmd[0], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')

wid_install_btn.on_click(install_btn)

@register_line_magic
def login_tool(line):
    clear_output()
    display(widgets.HBox([wid_password, wid_install_btn]))
