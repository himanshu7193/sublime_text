import sublime
import sublime_plugin
import re

todo_count = 0
status_key = "todo_scanner_status"
file_path = ""

class TodoScannerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global todo_count, file_path

        if self.view.file_name() and self.view.file_name().endswith(".md"):
            todos, done_todos = self.scan_todos()
            todo_count = len(todos)
            file_path = self.view.file_name()
            self.update_status()

    def scan_todos(self):
        content = self.view.substr(sublime.Region(0, self.view.size()))
        todos = re.findall(r'- \[ \] (.+?)(?=\n|$)', content, re.IGNORECASE)
        done_todos = re.findall(r'- \[x\] (.+?)(?=\n|$)', content, re.IGNORECASE)
        return todos, done_todos

    def update_status(self):
        global todo_count, file_path
        if file_path and file_path.endswith(".md"):
            status_text = f'TODOs: {todo_count} '
            self.view.set_status(status_key, status_text)

    def clear_status(self):
        self.view.erase_status(status_key)

class TodoScannerEventListener(sublime_plugin.EventListener):
    def on_load(self, view):
        view.run_command("todo_scanner")

    def on_modified(self, view):
        view.run_command("todo_scanner")

    def on_post_save(self, view):
        view.run_command("todo_scanner")

    def on_activated(self, view):
        view.run_command("todo_scanner")

    def on_close(self, view):
        if view.get_status(status_key).startswith("TODOs found"):
            view.run_command("todo_scanner_clear_status")


class TodoScannerClearStatusCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.erase_status(status_key)
