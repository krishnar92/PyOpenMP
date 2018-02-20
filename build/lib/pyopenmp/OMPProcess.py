import multiprocessing
import inspect
import time

class OMPProcess(object):
	"""private class representing the openmp process"""
	def __init__(self, _id = 0, target = None, args = tuple(), kwargs = dict()):
		super(OMPProcess, self).__init__()
		self.__id = _id
		self.__target = target
		self.__args = args
		self.__kwargs = kwargs
		self.__kwargs["procId"] = self.getProcessID()
		self.__process = multiprocessing.Process(target=self.__target, args=self.__args, kwargs=self.__kwargs)

	def start(self):
		"""starting the OMPProcess"""
		self.__process.start()

	def getProcessID(self):
		"""return the process id"""
		return self.__id

	def getProcessTarget(self):
		"""returns the process target function"""
		return self.__target

	def getTargetArgs(self):
		"""return the target args"""
		return self.__args

	def getTargetKwargs(self):
		"""return the target kwargs"""
		return self.__kwargs

	def join(self):
		self.__process.join()

	def wait(self,event):
		event.wait()
		


if __name__ == '__main__':
	def fun(*args, **kwargs):
		print " working " 	
		print kwargs
	process = OMPProcess(target=fun)
	process.start()
	process.join()