from .language import Language
from importlib.resources import files
import os

def load_language(filename):
	return Language.load(filename)

def set_language(language):
  LANGUAGE.copy(language)

_default_path = files('genespeak').joinpath('default.json')
# _directory = os.path.dirname(os.path.abspath(__file__))
# _default_lang_path = os.path.join(_directory, 'default.json')

LANGUAGE = load_language(_default_path)
