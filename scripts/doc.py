import os
import subprocess

os.makedirs("doc/api", exist_ok=True)
result = subprocess.run(['sphinx-build',
                         '-b',
                         'html',
                         'doc/source',
                         'doc/api'],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
if result.returncode == 0:
    print('✓ Docs genereated at doc/api')
else:
    print('✗ Docs generation failed')
