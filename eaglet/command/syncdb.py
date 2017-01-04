# -*- coding: utf-8 -*-
import os
from eaglet import peewee
import importlib

project_home = os.path.split(os.path.realpath(__file__))[0].split('.git')[0]
model_dict = {}
model_list = []
models_py_files = []


def __get_all_models_py(src):
	names = os.listdir(src)
	for name in names:
		srcname = os.path.join(src, name)
		if os.path.isdir(srcname):
			__get_all_models_py(srcname)
		if name == 'models.py':
			py_name = srcname.split(project_home + os.sep)[1].replace(os.sep, '.').replace('.py', '')

			models_py_files.append(py_name)

__get_all_models_py(project_home)


for models_py_file in models_py_files:
	print (type(models_py_file))
	models_module = importlib.import_module(models_py_file)
	for key, value in models_module.__dict__.items():
		if isinstance(value, peewee.BaseModel) and str(key) != 'Model':

			model_dict[key] = value
			model_list.append(value)

		print('----adas',type(value))

# import models2 as x


# for key, value in x.__dict__.items():
#     if isinstance(value, type) and issubclass(value, peewee.Model) and str(key) != 'Model':
#         model_dict[key] = value
#         model_list.append(value)
print(model_list)
# from t1.models import db
#
# db.create_tables(model_list,safe=True)


print(model_dict)
