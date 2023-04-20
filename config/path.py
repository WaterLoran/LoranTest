import os

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_PATH = os.path.join(BASE_PATH, 'config')
LOG_PATH = os.path.join(BASE_PATH, 'logs')

print("CONFIG_PATH", CONFIG_PATH)
print("BASE_PATH", BASE_PATH)
print("LOG_PATH", LOG_PATH)

