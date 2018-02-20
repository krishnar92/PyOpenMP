import random
import multiprocessing 


class ClauseShared(object):
	"""docstring for ClauseShared"""
	def __init__(self, shared_variables,kwargs):
		super(ClauseShared, self).__init__()
		self.__shared_variables = shared_variables
		self.__kwargs = kwargs

	def get_shared_variables(self):
		return self.__shared_variables

	def get_kwargs(self):
		return self.__kwargs

	def createShared(self):
		'''
		Supports list and dictionary

		'''
		if self.__shared_variables:			
			for eachVar in self.__shared_variables:
				if type(eachVar[1]) is type([]):
					self.__kwargs[eachVar[0]] = multiprocessing.Manager().list(eachVar[1])
				elif type(eachVar[1]) is type({}):
					self.__kwargs[eachVar[0]] = multiprocessing.Manager().dict(eachVar[1])
		
		return self.__kwargs

	def copyBack(self):
		if self.__shared_variables:
			for i in range(len(self.__shared_variables)):
				if type(self.__shared_variables[i][1]) is type([]):
					self.__shared_variables[i][1][:] = self.__kwargs[self.__shared_variables[i][0]]
				elif type(self.__shared_variables[i][1]) is type({}):
					self.__shared_variables[i][1].clear()
					self.__shared_variables[i][1].update(self.__kwargs[self.__shared_variables[i][0]])

#======================== How to use shared =====================================
#           only list and dictionaries
#	    list = [1,2,4]
#	    dict = {'a':1}
#	@OMPParallel(shared=(('list',list),('dict',dict))) # shared is a tuple of tuples each having name of the varible and its value - name can be anything
#	def fun(*args,**kwargs):
#		some code!	
# 		access by kwargs['name'] for list and dictionaries
#		
#	
#================================================================================
"""
	* Class for Private clause


"""
		
class ClausePrivate(object):

	"""
		* Parmeters
			- private_args(type - list) - the arguments which have to be private for each process
			
	"""
	def __init__(self,private_args):
		self.__args = private_args

	def  make_junk(self):
		for key in self.__args.keys():
			random.seed()
			self.__args[key] = random.randint(0,10000)

		return self.__args
if __name__ == "__main__":

	private_list = [1,2,3]
	privateObj = ClausePrivate(private_list)
	print privateObj.make_junk()
