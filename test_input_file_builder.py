import nose, os, itertools, shutil, multiprocessing
import numpy as np
from sets import Set

from nose.tools import with_setup
from parFDS import build_input_files, input_file_paths, build_pool

from helper_functions import dict_product, dict_builder, input_directory_builder,\
			     build_input_files, input_file_paths
#### tests ####

# Set the parameters
class Test_helper_methods(object):
	def __init__(self):
		self.x = {'a': [0,1], 'b': [2,3], 'c': [4]}
		self.test_name = 'STEP_BOX'
	
	def dict_product_len_test(self):
		y =  dict_product(self.x)
		assert len(list(y)) == 4

	def dict_builder_len_test(self):
		y =  dict_builder(self.x)
		assert len(list(y)) == 4

	def dict_product_vals_test(self):
		y =  dict_product(self.x)
		assert list(y) == [{'a': 0, 'b': 2, 'c': 4},
	 					  {'a': 0, 'b': 3, 'c': 4},
	 					  {'a': 1, 'b': 2, 'c': 4},
						  {'a': 1, 'b': 3, 'c': 4}]

	def dict_builder_vals_test(self):
		# dict_builder(params, test_name = '')
		y =  dict_builder(self.x, test_name = 'STEP_BOX')
		assert list(y) == [{'TITLE': 'STEP_BOX0-4-2', 'a': '0', 'b': '2', 'c': '4'},
							 {'TITLE': 'STEP_BOX0-4-3', 'a': '0', 'b': '3', 'c': '4'},
							 {'TITLE': 'STEP_BOX1-4-2', 'a': '1', 'b': '2', 'c': '4'},
							 {'TITLE': 'STEP_BOX1-4-3', 'a': '1', 'b': '3', 'c': '4'}]

	
class Test_build_input_files(object):
	def __init__(self):
		self.x = {'a': [0,1], 'b': [2,3], 'c': [4]}
		self.test_name = 'STEP_BOX'
		self.base_path = 'input_files'
		self.file_name = 'test.fds'
	
	def setup(self):
		build_input_files(self.file_name, self.x, 
				base_path = self.base_path, test_name = self.test_name)

	def teardown(self):
		shutil.rmtree(self.base_path)

	def build_input_files_test(self):
		file_list = Set(input_file_paths(self.base_path))
		vals = Set([os.path.join(os.getcwd(),'input_files/STEP_BOX0-4-2/STEP_BOX0-4-2.fds'),
			os.path.join(os.getcwd(),'input_files/STEP_BOX0-4-3/STEP_BOX0-4-3.fds'),
			os.path.join(os.getcwd(),'input_files/STEP_BOX1-4-2/STEP_BOX1-4-2.fds'),
			os.path.join(os.getcwd(),'input_files/STEP_BOX1-4-3/STEP_BOX1-4-3.fds')])
		assert Set(file_list) == Set(vals)

class Test_build_pool_1(object):
	def __init__(self):
		pass

	def setup(self):
		self.pool = build_pool(multiproc = True, pool_size = None)
		#print ("TestUM:setup() before each test method")
 
	def teardown(self):
		self.pool.terminate() 
		#print ("TestUM:teardown() after each test method")

	def build_pool_type_test(self):
		assert type(self.pool) is multiprocessing.pool.Pool

	def build_pool_children_test(self):
		assert len(multiprocessing.active_children()) == 2

class Test_build_pool_2(object):
	def __init__(self):
		pass
		
	def setup(self):
		self.pool = build_pool(multiproc = True, pool_size = -1)
 
	def teardown(self):
		self.pool.terminate() 

	def build_pool_type_test(self):
		assert type(self.pool) is multiprocessing.pool.Pool

	def build_pool_children_test(self):
		assert len(multiprocessing.active_children()) == multiprocessing.cpu_count()


def directory_builder1_setup():
	input_directory_builder('test_123', 'input_files')

def directory_builder1_teardown():
	shutil.rmtree('input_files')

@with_setup(directory_builder1_setup,
 			directory_builder1_teardown)
def input_directory_builder_test1():
	dirpath_list = []
	dirname_list = []
	for dirpath, dirnames, filenames in  os.walk(os.path.join(os.getcwd(),'input_files/')):
	    dirpath_list.append(dirpath) 
	    dirname_list.append(dirnames)

	assert dirpath_list == [os.path.join(os.getcwd(),'input_files/'),
							os.path.join(os.getcwd(),'input_files/test_123')]
	assert dirname_list == [['test_123'], []]

def directory_builder2_setup():
    input_directory_builder('test_123', 'input_files')
    input_directory_builder('test_234', 'input_files')

def directory_builder2_teardown():
    shutil.rmtree('input_files')

@with_setup(directory_builder2_setup,
 			directory_builder2_teardown)
def input_directory_builder_test2():
	dirpath_list = []
	dirname_list = []
	for dirpath, dirnames, filenames in  os.walk('input_files/'):
	    dirpath_list.append(dirpath) 
	    dirname_list.append(dirnames)
	assert Set(dirpath_list) == Set(['input_files/', 'input_files/test_123', 'input_files/test_234'])
	assert Set(dirname_list[0]) == Set(['test_123', 'test_234'])
