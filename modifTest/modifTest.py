from krita import *
from time import time
from PyQt5.QtCore import QObject, QEvent
# from PyQt5.QtGui import QGuiApplication

from .currentTool import getCurrentTool


TOOLS = [
("Freehand selection (toggle)", "KisToolSelectOutline"),
("Gradient (toggle)", "KritaFill/KisToolGradient"),
("Line tool (toggle)", "KritaShape/KisToolLine"),
("Transform tool (toggle)", "KisToolTransform"),
("Move tool (toggle)", "KritaTransform/KisToolMove")
]

def setTool(toolName):
	Application.instance().action(toolName).trigger()

def setBrushTool():
	setTool("KritaShape/KisToolBrush")

def isToolSelected(toolName):
	if getCurrentTool() == toolName: return True
	else: return False



class Filter(QMdiArea):
	def __init__(self, setLowFunction, setHighFunction, isHighStateFunction, relatedTool, parent=None):
		super().__init__(parent)

		self.installEventFilter(self)
		self.keyReleased = False
		self.updateTime()

		self.setLowFunction = setLowFunction
		self.setHighFunction = setHighFunction
		self.isHighStateFunction = isHighStateFunction
		self.relatedTool = relatedTool
		
	def updateTime(self):
		self.t = time()

	def keyPress(self):
		print("tool ON")
		self.keyReleased = False
		self.updateTime()

		self.state = self.isHighStateFunction(self.relatedTool[1])
		if not self.state: #low
			self.setHighFunction(self.relatedTool[1])

	def keyRelease(self):
		print("tool OFF")
		self.keyReleased = True

		if time() - self.t > 0.3 or self.state:
			self.setLowFunction()

	def eventFilter(self, obj, e):
		if e.type() == QEvent.KeyRelease:
			if (Krita.instance().action(self.relatedTool[0]).shortcut().matches(e.key()) > 0
			and not e.isAutoRepeat()
			and not self.keyReleased):
				self.keyRelease()

		return False




class modifTest(Extension):

	def __init__(self, parent):
		super(modifTest, self).__init__(parent)
		self.filters = []

	def setup(self):
		pass

	def createActions(self, window):

		for tool in TOOLS:
			action = window.createAction(tool[0], tool[0], "tools/scripts")
			action.setAutoRepeat(False)
			self.filters.append(Filter(setBrushTool, setTool, isToolSelected, tool))
			action.triggered.connect(self.filters[-1].keyPress)

		# tool = TOOLS[0]
		# action = window.createAction("test", "test", "tools/scripts")
		# action.setAutoRepeat(False)
		# self.filter = Filter(setBrushTool, setTool, brushNotSelected, tool)
		# action.triggered.connect(self.filter.keyPress)




Krita.instance().addExtension(modifTest(Krita.instance()))
