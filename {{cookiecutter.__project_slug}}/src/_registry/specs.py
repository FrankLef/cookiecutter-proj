from config import settings

from fltk.specs.load_specs import load_specs

data_path = settings.paths.data

specs_mstr = load_specs("example", path=data_path)
