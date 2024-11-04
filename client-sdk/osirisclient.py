import sys
import os

path1 = './core'
path2 = './advanced-features'

if os.path.exists(os.path.join(path1, 'core.py')):
    sys.path.insert(0, path1)
    from core import *
    sys.path.pop(0)
else:
    raise FileNotFoundError("Core file (./core/core.py) not found, check to make sure you set up the SDK correctly")

if os.path.exists(os.path.join(path2, 'advancedfeatures.py')):
    sys.path.insert(0, path2)
    from advancedfeatures import *
    sys.path.pop(0)
else:
    raise FileNotFoundError("Advanced features file (./advanced-features/advancedfeatures.py) not found, check to make sure you set up the SDK correctly")
