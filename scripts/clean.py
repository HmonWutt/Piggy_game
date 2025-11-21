import shutil
from codecs import ignore_errors

shutil.rmtree('__pycache__', ignore_errors=True)
shutil.rmtree('package/__pycache__', ignore_errors=True)
shutil.rmtree('test/__pycache__', ignore_errors=True)
shutil.rmtree('.pytest_cache', ignore_errors=True)
shutil.rmtree('doc/api/', ignore_errors=True)
shutil.rmtree('doc/uml/', ignore_errors=True)
shutil.rmtree('htmlcov', ignore_errors=True)
shutil.rmtree('data/', ignore_errors=True)
print("Cleanup complete")
