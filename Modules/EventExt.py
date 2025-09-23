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

import datetime

class EventExt:
	"""
	EventExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		self.Name = parent().par.Name.eval()
		self.Description = parent().par.Description.eval()
		self.Id = parent().par.Id.eval()

		self.Time = datetime.time(hour=parent().par.Time1.eval(), minute=parent().par.Time2.eval(), second=parent().par.Time3.eval())
		self.Delay = parent().par.Delay * 1000

		self.OnStart = parent().par.Onstart.eval()
		self.OnClose = parent().par.Onclose.eval()

		self.Task = op('task').text
		
	def is_active(self):
		return parent.Event.par.Active.eval()

	def RunTask(self):
		if self.is_active():
			run(self.Task, fromOP=parent.Event, asParameter=True, delayMilliSeconds = self.Delay)