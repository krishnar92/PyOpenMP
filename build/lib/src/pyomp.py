from OMPPool import *
import functools
import random
from clauses import *

class OMPParallel(object):
	"""implemantation for parallel directive - OMPParallel"""
	def __init__(self, numprocs = 4, condition = True, private = None, shared = None, firstprivate = None):
		super(OMPParallel, self).__init__()
		self.numprocs = numprocs
		self.private = private
		self.shared = shared
		self.firstprivate = firstprivate
		self.condition = condition

	def __call__(self, target):
		""" decorator function for the target function """

		def wrapper(*args, **kwargs):
			# check the condition
			if not self.condition:
				# condition is false so dont create team of processes
				apply(target, args, kwargs)
			else:
				# condition is true, create team of processes
				if self.private: 
					self.private = ClausePrivate(self.private).make_junk()					
				shared_object = ClauseShared(self.shared,kwargs)
				kwargs = shared_object.createShared()
				OMPParallel.pool = OMPPool(numprocs = self.numprocs, target = target, args = args, kwargs = kwargs)
				OMPParallel.pool.start()
				OMPParallel.pool.join()
				shared_object.copyBack()



		return functools.wraps(target) (wrapper)

	@classmethod
  	def returnPool(cls):
  		return OMPParallel.pool

class OMPFor(object):
	"""implementation for openmp for directive - OMPFor"""
	def __init__(self, args = tuple(), kwargs = dict()):
		super(OMPFor, self).__init__()
		self.__args = args
		self.__kwargs = kwargs
		self.__numProcs = kwargs["poolCount"]
		self.__procId = kwargs["procId"]

	def __call__(self, target):
		""" decorator function for the target For function """

		def wrapper(iterable, *args, **kwargs):

			if not hasattr(iterable, '__len__'):
				iterable = list(iterable)

			self.__iterable = iterable
			chunks = self.__getChunks()

			# current processess chunk of iterable
			self.__kwargs["start"] = chunks[self.__kwargs["procId"]][0]
			self.__kwargs["end"] = chunks[self.__kwargs["procId"]][1]

			# execute the target function
			target(iterable, *self.__args, **self.__kwargs)

		return functools.wraps(target) (wrapper)	

	def __getChunks(self):
		""" get the chunks to be executed by each process """
		
		chunk, extra = divmod(len(self.__iterable), self.__numProcs)
		chunks = [chunk for i in range(self.__numProcs)]
		if extra:
		 	for i in range(len(chunks)):
				if extra:
					chunks[i] = chunks[i] + 1
					extra = extra - 1
				else:
		 			break

		start = 0
		end = 0
		
		# list of tuples representing the start and end indexes
		result = []

		for i in range(self.__numProcs):
			end = end + chunks[i]
			result.append((start, end))
			start = end

		return result

class OMPMaster(object):

	def __init__(self,args=tuple(),kwargs = dict()):
		self.__args = args
		self.__kwargs = kwargs
		self.procId = kwargs["procId"]

	def __call__(self,function):

		def wrapper(*args,**kwargs):
			if self.procId == 0:
				function(*self.__args,**self.__kwargs)
			else:
				pass
		return wrapper

class OMPSingle(OMPParallel):
	def __init__(self,args=tuple(),kwargs= dict()):
		self.__args = args
		self.__kwargs = kwargs
		self.__procId = kwargs["procId"]
		self.__numProcs = kwargs["poolCount"]
		self.__randomProcessNumber = kwargs["randomProcessNumber"]
		self.__pool = OMPParallel.returnPool()
		self.__eventForSingleExecution = kwargs["eventForSingleExecution"]
		self.__eventForSingleEncounter = kwargs["eventForSingleEncounter"]

	def __call__(self, function):
		def wrapper(*args, **kwargs):
			if self.__procId == self.__numProcs - 1:
				self.__eventForSingleEncounter.set()

			self.__eventForSingleEncounter.wait()
			if self.__procId == self.__randomProcessNumber:
				function(*self.__args,**self.__kwargs)
				self.__eventForSingleExecution.set()			

			else:
				self.__pool.getProcessForID(self.__procId).wait(self.__eventForSingleExecution)
			
		return wrapper
