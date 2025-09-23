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

class SchedulerExt:
	"""
	SchedulerExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		self.Scheduled = parent().par.Scheduled.eval()

		if self.Scheduled:
			# Getting current date
			current_date = datetime.date.today()
			# Getting the day name
			day_name = current_date.strftime("%A")
			schedule = op.PARS.Show["scheduler"][day_name]

			self.Start = datetime.time(hour=int(schedule.split(" - ")[0].split(":")[0]), minute=int(schedule.split(" - ")[0].split(":")[1]), second=int(schedule.split(" - ")[0].split(":")[2]))
			self.End = datetime.time(hour=int(schedule.split(" - ")[1].split(":")[0]), minute=int(schedule.split(" - ")[1].split(":")[1]), second=int(schedule.split(" - ")[1].split(":")[2]))
		else:
			self.Start = datetime.time(hour=0, minute=0, second=0)
			self.End = datetime.time(hour=0, minute=0, second=0)
		# properties
		TDF.createProperty(self, 'Events', value=list(), dependable="deep", readOnly=False)
		
		if op('opfind_events').valid:
			self.AddEventCOMPs()
			
		self.ReinitEvents()

	def AppendEvent(self, event):
		self.Events.append(event)

	def RemoveEvent(self, event):
		self.Events.remove(event)

	def GetEvent(self, index):
		return self.Events[index]

	def GetEvents(self):
		return self.Events
	
	def AddEventCOMPs(self):
		list = op('opfind_events')
		for event in list.rows():
			if event[0] != 'name':
				if op(event[0]) not in self.Events:
					self.AppendEvent(op(event[0]))
					
	def ReinitEvents(self):
		for event in self.Events:
			event.par.reinitextensions.pulse()

	def OnStart(self):
		for event in self.Events:
			if event.OnStart:
				event.RunTask()

	def OnClose(self):
		for event in self.Events:
			if event.OnClose:
				event.RunTask()

	def TriggerTime(self, h=0, m=0, s=0):
		time = datetime.time(hour=int(h), minute=int(m), second=int(s))
		self.CheckTasksAtTime(time,True)

	def CheckTasksAtTime(self, time, run):
		current_tasks = list()
		for event in self.Events:
			if time == event.Time:
				current_tasks.append(event)
				if run:
					event.RunTask()
					if self.Logger:
						self.Logger.Info('Ran task of event: ' + event.Name + ' at ' + str(event.Time))
		return current_tasks

	@property
	def Logger(self):
		return op('logger')