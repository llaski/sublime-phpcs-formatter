import os
import sys
import shlex
import ntpath
import subprocess
import sublime
import sublime_plugin
import re

def debug_message(msg):
    print("[PHPCS Formatter] " + str(msg))

class PHPCSFormatterCommand(sublime_plugin.WindowCommand):
    def get_paths(self):
        file_path = self.window.active_view().file_name()
        app_path = self.find_app_path(file_path)

        directory = self.directory = os.path.dirname(os.path.realpath(file_path))

        file_name = file_path.split('/').pop()

        active_view = self.window.active_view()

        return file_name, app_path, active_view, directory

    def find_app_path(self, file_name):
        app_path = file_name
        found = False
        while found == False:
            app_path = os.path.abspath(os.path.join(app_path, os.pardir))
            found = os.path.isfile(app_path + '/package.json') or app_path == '/'
        return app_path

    def parse_report(self, command):
        report = self.shell_out(command)
        debug_message(report)
        # lines = re.finditer('.*(?P<line>\d+)\) (?P<file>.*)', report)

        # for line in lines:
        #     error = CheckstyleError(line.group('line'), line.group('file'))
        #     self.error_list.append(error)

    def shell_out(self, cmd):
        self.error_list = []
        self.workingDir = self.directory

        data = None

        info = None
        if os.name == 'nt':
            info = subprocess.STARTUPINFO()
            info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            info.wShowWindow = subprocess.SW_HIDE

        debug_message("cwd: " + self.workingDir)
        debug_message("cmd: " + cmd)
        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=info, cwd=self.workingDir)

        if proc.stdout:
            data = proc.communicate()[0]

        return data.decode()

    # def run_in_terminal(self, command):
    #     settings = sublime.load_settings("Preferences.sublime-settings")
    #     terminal_setting = settings.get('phpunit-sublime-terminal', 'Terminal')

    #     osascript_command = 'osascript '
    #     osascript_command += '"' + os.path.dirname(os.path.realpath(__file__)) + '/run_command.applescript"'
    #     osascript_command += ' "' + command + '"'
    #     osascript_command += ' "PHPUnit Tests"'

    #     os.system(osascript_command)

class runPhpcsFormatCommand(PHPCSFormatterCommand):

    def run(self, *args, **kwargs):
        file_name, app_path, active_view, directory = self.get_paths()
        command = '/Users/larrylaski/.composer/vendor/bin/php-cs-fixer fix ' + file_name + ' --rules=@PSR2,psr4 --allow-risky="yes" --verbose'


        self.parse_report(command)
