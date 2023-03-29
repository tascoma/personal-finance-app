import sys
import os

module_path = os.path.join(os.path.dirname(__file__), '..')
if module_path not in sys.path:
    sys.path.append(module_path)
