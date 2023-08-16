import os
import sys

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
COMMON_PATH = os.path.join(BASE_PATH, 'common')
CONFIG_PATH = os.path.join(BASE_PATH, 'config')
CORE_PATH = os.path.join(BASE_PATH, 'core')
LOG_PATH = os.path.join(BASE_PATH, 'logs')
FILES_PATH = os.path.join(BASE_PATH, 'files')
PAGES_PATH = os.path.join(BASE_PATH, 'pages')


sys.path.append(BASE_PATH)
sys.path.append(COMMON_PATH)
sys.path.append(CONFIG_PATH)
sys.path.append(CORE_PATH)
sys.path.append(LOG_PATH)
sys.path.append(PAGES_PATH)

sys.path.append(os.getcwd())

print("os.getcwd()", os.getcwd())

print("CONFIG_PATH", CONFIG_PATH)
print("BASE_PATH", BASE_PATH)
print("LOG_PATH", LOG_PATH)
print("PAGES_PATH", PAGES_PATH)

print("sys.path", sys.path)



