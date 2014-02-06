import nose, os, shutil, multiprocessing
from sets import Set

from nose.tools import with_setup
from parFDS import build_input_files, input_file_paths, build_pool

from helper_functions import dict_product, dict_builder, input_directory_builder,\
			     build_input_files, input_file_paths
#### tests ####	
class Test_build_input_files(object):
	def __init__(self):
		self.x = {'a': [0,1], 'b': [2,3], 'c': [4]}
		self.test_name = 'STEP_BOX'
		self.base_path = 'input_files'
		self.file_name = './tests/input_file_builder.fds'
	
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
