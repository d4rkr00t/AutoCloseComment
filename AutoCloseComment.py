import sublime, sublime_plugin

class AutoCssCloseCommentCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.coursor_pos = self.view.sel()[0].begin()
		self.edit = edit
		self.comment_on_nl = False

		if "less" in self.view.syntax_name(self.view.sel()[0].b):
			self.comment_on_nl = True

		if "css" in self.view.syntax_name(self.view.sel()[0].b) or "less" in self.view.syntax_name(self.view.sel()[0].b):
			#expand selection
			self.view.run_command("expand_selection", {"to": "brackets"})
			self.view.run_command("expand_selection", {"to": "line"})

			sels = self.view.sel() 

			self.process_selection(sels)


	def add_comment(self, selected, insert_place):
		tag = self.get_tag(selected)

		self.view.insert(self.edit, insert_place, self.fromat_close_tag(tag))

		self.view.sel().clear()
		self.view.sel().add(sublime.Region(self.coursor_pos, self.coursor_pos))
		

	def process_selection(self, sels):
		# Get text and strip spaces and tabs
		selected = self.view.substr(sels[0])
		selected = selected.strip(' \t\n\r')

		# Calculate comment insert place
		# insert_place = sels[0].end()-steps_back
		insert_place = sels[0].begin()+self.view.substr(sels[0]).rfind('}')+1


		# If first char != { then find and insert comment
		# if selected[0] == '.' or selected[0] == '#' or selected[0] == '&':
		if selected[0] != '{':
			print sels[0].begin()
			self.add_comment(selected, insert_place)
		else:
			# If first char == { then extend selection
			self.view.sel().add(sublime.Region(sels[0].a-1, insert_place-2))
			self.view.run_command("expand_selection", {"to": "line"})
			self.process_selection(self.view.sel())


	def get_tag(self, string):
		# find all from start to {
		open_bracket = string.find('{')
		return string[0:open_bracket]


	def fromat_close_tag(self, tag):
		# format comment
		if self.comment_on_nl:
			return "\n/* %s */" % tag.strip(' \t\n\r')
		else:
			return " /* %s */" % tag.strip(' \t\n\r')

		