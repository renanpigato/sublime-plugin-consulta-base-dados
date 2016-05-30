import sublime, sublime_plugin, subprocess, re, json, pprint

class ConsultaBaseDadosCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		fileName      = self.view.file_name();
		fileExtension = re.search(".*\.sql$", fileName);
		
		if(fileExtension == None):
			sublime.message_dialog("Este NÃO é um arquivo de SQL cara!!");
			return;
		
		self.execute(fileName);

	def execute(self, fileName):

		sqlCommand = self.constructCommand(fileName);

		try:
			response = subprocess.check_output(sqlCommand, stderr=subprocess.STDOUT, shell=True).decode('utf8');
		except e:
			response = e;

		self.openTerminal(response);

	def constructCommand(self, fileName):

		host = sublime.load_settings('ConsultaBaseDados.sublime-settings').get('host')     #"localhost";
		port = sublime.load_settings('ConsultaBaseDados.sublime-settings').get('porta')    #"5432";
		user = sublime.load_settings('ConsultaBaseDados.sublime-settings').get('usuario')  #"postgres";
		base = sublime.load_settings('ConsultaBaseDados.sublime-settings').get('base')     #"agrofiusa";
		
		return "psql -h " + host + " -p " + port + " -U " + user + " " + base + " -f " + fileName;

	def openTerminal(self, txt):

		self.output_view = self.view.window().create_output_panel("textarea");
		window = sublime.active_window();
		window.run_command("show_panel", {"panel": "output.textarea"});
		self.output_view.set_read_only(False);
		self.output_view.run_command("append", {"characters": txt});