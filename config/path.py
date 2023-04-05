import os


CONFIG_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
BASE_PATH = os.path.split(CONFIG_PATH)[0]
LOG_PATH = os.path.join(BASE_PATH, 'logs')

print("CONFIG_PATH", BASE_PATH)
print("BASE_PATH", BASE_PATH)
print("LOG_PATH", LOG_PATH)

