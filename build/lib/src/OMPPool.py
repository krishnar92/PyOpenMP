import OMPProcess
import multiprocessing
import random

class OMPPool(object):
	"""creates a pool of OMPProcessess"""
	def __init__(self, numprocs = None, target=None, args = None, kwargs = None):
		super(OMPPool, self).__init__()
		self.__numprocs = numprocs
		self.__target = target
		self.__args = args
		self.__kwargs = kwargs
		self.__kwargs["poolCount"] = self.getPoolCount()
		self.__kwargs["randomProcessNumber"] = random.randint(0,self.__numprocs -1)
		self.__kwargs["eventForSingleExecution"] = multiprocessing.Event()
		self.__kwargs["eventForSingleEncounter"] = multiprocessing.Event()
		self.__processes = [OMPProcess.OMPProcess(_id=i, target=self.__target, args = self.__args, kwargs = self.__kwargs) for i in range(numprocs)]

	def getPoolTarget(self):
		""" returns the target function for this pool """
		return self.__target

	def getPoolArgs(self):
		""" returns the arguments for the target in this pool """
		return self.__args

	def getPoolKwargs(self):
		""" return the kwargs for the target in this pool """
		return self.__kwargs

	def getPoolCount(self):
		""" returns the number of processes in this pool """
		return self.__numprocs

	def start(self):
		""" start the pool """
		for process in self.__processes:
			process.start()

	def join(self):
		""" end the pool """
		for process in self.__processes:
			process.join()

	def getProcessForID(self, _id):
		""" return the process with given id """
		for process in self.__processes:
			if process.getProcessID() == _id:
				return process
		return None