"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

from TDStoreTools import StorageManager
import TDFunctions as TDF

import json

class ParametersExt:
	"""
	ParametersExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		# properties
		TDF.createProperty(self, 'Data', value=op("pars").result, dependable=True, readOnly=False)
		self.create_dict()

	def create_dict(self):
		for data in self.Data:
			TDF.createProperty(self, data, value=self.Data[data], dependable=True, readOnly=False)
	
	def Update(self):
		self.Data = op("pars").result
		self.create_dict()

	@property
	def Get(self):
		return op("pars").result