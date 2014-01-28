import os, itertools, shutil
import numpy as np

def dict_product(dicts):
	"""
	dict_product(dicts)

	from a dict of parameters creates a generator which outputs a list of dicts 
	effectively a cartesian product over the parameter space.

	eg: from:  	{'a': [0,1], 'b': [2,3], 'c': [4]}

	outputs:   [{'a': 0, 'b': 2, 'c': 4},
			  	{'a': 0, 'b': 3, 'c': 4},
			  	{'a': 1, 'b': 2, 'c': 4},
	      		{'a': 1, 'b': 3, 'c': 4}]
	"""
	# from http://stackoverflow.com/questions/5228158/cartesian-product-of-a-dictionary-of-lists
	return (dict(itertools.izip(dicts, x)) for x in itertools.product(*dicts.itervalues()))

def dict_builder(params, test_name = ''): 
	"""
	dict_builder(params)

	uses the dict_product function and adds a 
	title key value pair for use in the input files
	
	eg: from:  	{'a': [0,1], 'b': [2,3], 'c': [4]}

	outputs:    [{'TITLE': 'STEP_BOX0-4-2', 'a': '0', 'b': '2', 'c': '4'},
				 {'TITLE': 'STEP_BOX0-4-3', 'a': '0', 'b': '3', 'c': '4'},
				 {'TITLE': 'STEP_BOX1-4-2', 'a': '1', 'b': '2', 'c': '4'},
				 {'TITLE': 'STEP_BOX1-4-3', 'a': '1', 'b': '3', 'c': '4'}]
	"""

	for value_set in dict_product(params):
		title = "-".join(map(str, value_set.values())).replace('.', '_')
		vals = [dict([a, str(x)] for a, x in value_set.iteritems())]
		vals = vals[0]
		vals['TITLE'] = test_name + title
		yield vals

def input_directory_builder(folder_name, base_path):
	"""
	input_directory_builder(folder_name, base_path)

	taking a base_path and a particular folder (folder_name) and creating both 
	folder_name inside of base_path if base_path does not exist and if base_path
	does exist, just creates folder_name inside of it.
	"""
	calling_dir = os.getcwd()
	
	if not os.path.exists(os.path.join(calling_dir, base_path)):
		os.mkdir(base_path)

	try:
		os.chdir(os.path.join(calling_dir, base_path))
		os.mkdir(folder_name)
	except:
		raise
	finally:
		os.chdir(calling_dir)

def build_input_files(base_file, params, base_path = 'input_files', test_name = ''):
	"""
	build_input_files(base_file, params, base_path = 'input_files')

	takes a 'well-formated' input file, a set of parameters in a dict, 
	and outputs a directory structure with the properly formated input files
	created in them. 
	"""
	calling_dir = os.getcwd()

	with open(base_file, 'r') as f:
		txt = f.read()

	for value_set in dict_builder(params, test_name = test_name):
		tmp_txt = txt
		# make a directory
		input_directory_builder(value_set['TITLE'], base_path)
		# populate the input file
		tmp_txt = tmp_txt.format(**value_set)
		# create the file name
		fname = os.path.join(calling_dir, base_path, 
					value_set['TITLE'], value_set['TITLE']+'.fds')
		# write the input file to the directory
		with open(fname, 'w') as f:
			f.write(str(tmp_txt))

def input_file_paths(base_path):
	"""
	input_file_paths(base_path) 

	returns the paths of the input files present by recusivly walking over them
	so they can be iterated over in the main body of the program via multiprocessing
	"""
	paths = []
	for dirpath, dirnames, filenames in os.walk(base_path):
	    for onefile in filenames:
	    	# the following if statement is due to OS X .DsStore bullshit...
	    	if not onefile.startswith('.DS'):
		        #paths.append(dirpath+"/"+onefile)      
		        paths.append(os.path.join(os.getcwd(), dirpath, onefile))
	return paths
