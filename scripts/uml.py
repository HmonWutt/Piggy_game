import os
import subprocess

os.makedirs("doc/uml", exist_ok=True)
result = subprocess.run(
    ["pyreverse", "-o", "png", "-p", "uml", "package/", "-d", "doc/uml/"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
if result.returncode == 0:
    print("✓ UML diagrams saved to doc/uml")
else:
    print("✗ Uml generation failed")
