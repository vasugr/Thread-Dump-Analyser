import sublime
import sublime_plugin
from . import controller


def analyze_thread_dump1(thrddump):
	return "ok\t huehuehue\n\n\n\n\n\n\n\nhue"

class TdaCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		allcontent = sublime.Region(0, self.view.size())   
		print("Analyzing thread dump...\n")
		text = self.view.substr(allcontent).strip()
		result,Folder = controller.generateSummary(text)

		self.view.replace(edit, allcontent, result)
		self.view.fold(Folder)
		sublime.status_message("Done!")