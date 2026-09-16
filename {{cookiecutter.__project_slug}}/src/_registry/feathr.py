from config import settings

from fltk.feathr.feathr import Feathr

data_path = settings.paths.data

nms = ("sales", "sales_outl", "sales_encc", "sales_enct", "survey_amts")
feathr = Feathr(data_path, names=nms)
