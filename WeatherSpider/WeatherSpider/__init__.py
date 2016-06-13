import os.path
import sys

dirname = os.path.dirname
sys.path.append(dirname(dirname(dirname(__file__))))

from WeatherServer import app
