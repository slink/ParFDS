import os, itertools, shutil, glob, multiprocessing, subprocess
import numpy as np
import pandas as pd
from matplotlib import pylab as plt
from helper_functions import dict_product, dict_builder, input_directory_builder
from helper_functions import build_input_files, input_file_paths

def build_pool(multiproc = True, pool_size = None):
	"""
	build_pool(multiproc = True, pool_size = None)

	if multiproc == True creates a pool using multiprocessing.Pool
	False will eventually implement a way to use the IPython cluster module instead

	pool_size is the number of workers to use.
	values are from 0 to n
	if None, a default value of 2 is set. 
	if -1, multiprocessing.cpu_count() is set.
	"""
	if not pool_size:
		pool_size = 2
	elif pool_size == -1:
		pool_size = multiprocessing.cpu_count()
	elif not isinstance(pool_size, int):
		raise TypeError
	
	if multiproc:
		# pool_size = multiprocessing.cpu_count() * 2
		pool = multiprocessing.Pool(processes=pool_size)
		return pool
	else:
		raise TypeError

def fds_calculation(input_path):
	"""
	fds_calculation(input_path) 

	assumes a valid input path has been passed to it. The function then does
	a subprocess call (effectivly to the command line) to then run an mpirun 
	job with the flag -np set to 'proc_per_simulation' (which is unfortunatly 
	currently hard coded in this function)
	"""
	proc_per_simulation = 1

	cur_dir = os.getcwd()
	(input_path, input_file) = os.path.split(input_path)
	(input_head, input_ext) = os.path.splitext(input_file)
	os.chdir(input_path)
	retcode = subprocess.call(['mpirun', '-np', str(proc_per_simulation),\
					 'fds_mpi', input_file, '&>', input_head + '.err', '&'])
	os.chdir(cur_dir)
	return retcode

def main(input_file, parameters, **kwargs):
	build_input_files(input_file, parameters, 
					  base_path = kwargs['base_path'], 
					  test_name = kwargs['test_name'])
	paths = input_file_paths(kwargs['base_path'])
	pool = build_pool(multiproc = kwargs['multiproc'], 
					  pool_size = kwargs['pool_size'])
	#types = [type(x) for x in paths]
	#print type(kwargs['funct']), types
	# pool_outputs = pool.map(kwargs['funct'], paths)
	pool_outputs = pool.map(fds_calculation, paths)

	pool.close()
	return pool_outputs

def plotter(parameters, plotted_val = 'HRR',  **kwargs):
	"""
	plotter(parameters, plotted_val = 'HRR',  **kwargs)

	takes in a parameter set and a plotted_val (for now a column label in the FDS output)
	reads the data in, and then plots all grouping variations of the plotted_val as a function 
	of the parameter study variables.
	"""
	dataLists = {}  
	# read data  
	for folder in glob.glob(os.path.join(kwargs['base_path'],'*')):  
		for datafile in glob.glob(os.path.join(folder, '*_hrr.csv')): 
			dataLists[folder.split("/")[-1]] = pd.read_csv(datafile, skiprows = 1) 
	
	filename_map = pd.DataFrame(list(dict_builder(parameters, test_name = kwargs['test_name'])))
	for key in parameters.keys():
		for results in filename_map.groupby(by = key):
			plt.figure()
			for title in results[1]['TITLE'].values:
				plt.plot(dataLists[title].Time, dataLists[title][plotted_val], label = title)
			plt.title(key + ' ' + str(results[0]))
			plt.legend()
			plt.savefig(key + ' ' + str(results[0]) + '.png', dpi = 300)

if __name__ == '__main__':
	input_file = 'StepBoxDan.fds'
	parameters = {'STEP_WMAX': np.linspace(0.05,0.4,4), 
				  'WALL_TEMP': np.ceil(np.linspace(50, 200, 4)), 
				  'COLD_TEMP': [25.0]}
	kwargs = {'test_name' : 'StepBoxDan', 
			  'base_path' : 'input_files', 
			  'funct' : fds_calculation,
			  'multiproc' : True, 
			  'pool_size' : 4}

	calling_dir = os.getcwd()
	
	if os.path.exists(os.path.join(calling_dir, kwargs['base_path'])):
		shutil.rmtree(os.path.join(calling_dir, kwargs['base_path']))

	main(input_file, parameters, **kwargs)
	plotter(parameters, plotted_val = 'HRR',  **kwargs)