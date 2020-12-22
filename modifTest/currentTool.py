from krita import Krita
from PyQt5.QtWidgets import QWidget, QToolButton

def find_tool_box(qwindow):
    for qobj in qwindow.findChildren(QWidget):
        if qobj.metaObject().className() == "KoToolBox":
            return qobj


def find_active_tool(qtoolbox):
    for qobj in qtoolbox.findChildren(QToolButton):
        if qobj.metaObject().className() == "KoToolBoxButton":
            if qobj.isChecked():
                return qobj

def find_my_current_tool():
    app = Krita.instance()
    qwindow = app.activeWindow().qwindow()
    tool_box = find_tool_box(qwindow)
    tool = find_active_tool(tool_box)
    return tool

def getCurrentTool():
	tool = find_my_current_tool()
	name = tool.objectName()
	return name
	# checked = tool.isChecked()
	# print("tool: {tool}, tool.objectName: {name}, checked: {checked}".format(**locals()))