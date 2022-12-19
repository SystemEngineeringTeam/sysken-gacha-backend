import urllib3
import os
from dotenv import load_dotenv

file = urllib3.PoolManager().request('GET', 'https://raw.githubusercontent.com/akameco/akameco/master/scripts/mig-remote-column.py')
print(file.data)