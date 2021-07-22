import sublime
import sublime_plugin
from . import controller


class TdaCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		allcontent = sublime.Region(0, self.view.size())   
		print("Analyzing thread dump...\n")
		fname = self.view.file_name()
		#print("file name == "+fname + "\n")
		text = self.view.substr(allcontent).strip()
		result,Folder = controller.generateSummary(text)

		#out_filename = fname[:-4] + "_output.txt"
		#f2 = open(out_filename, "w+")
		#f2.write(result)
		#f2.close()
		
		#sublime.active_window().open_file(out_filename)
		#view2 = sublime.active_window().active_view()
		#print(" view1 = "+str(self.view) + "view2 = "+str(view2))
		self.view.replace(edit, allcontent, result)
		self.view.fold(Folder)

		#newcontent = sublime.Region(0, view2.size())
		#view2.replace(edit, newcontent, result)
		#view2.fold(Folder)
		print("\ndone...\n")
		sublime.status_message("Done!")