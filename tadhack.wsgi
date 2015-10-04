activate_this = '/path/to/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
sys.path.insert(0,'/home/ubuntu/tadhack')
from app import {app global variable in app.py} as application
