import sys
import time
import json
import pytest
import allure
from easydict import EasyDict as register

from config.path import BASE_PATH
from config.path import COMMON_PATH
from config.path import CONFIG_PATH
from config.path import CORE_PATH
from config.path import LOG_PATH
from config.path import FILES_PATH
from config.path import PAGES_PATH

sys.path.append(BASE_PATH)
sys.path.append(COMMON_PATH)
sys.path.append(CONFIG_PATH)
sys.path.append(CORE_PATH)
sys.path.append(LOG_PATH)
sys.path.append(FILES_PATH)
sys.path.append(PAGES_PATH)

from core.event import *



