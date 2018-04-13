import sublime
import sublime_plugin

SPLIT_AT_DEFAULT = 40
_split_at = SPLIT_AT_DEFAULT

class IndentToSplitCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        for region in self.view.sel():
            text = self.view.find("[^\s]|$", region.begin())
            begin_row, col = self.view.rowcol(text.begin())
            end_row, _ = self.view.rowcol(region.end())

            if (col < _split_at):                    
                insert_string = " " * (_split_at - col)
                for row in range(begin_row, end_row + 1):
                    insert_point = self.view.text_point(row, col)
                    self.view.insert(edit, insert_point, insert_string)

            elif (col > _split_at):
                offset = col - _split_at
                for row in range(begin_row, end_row + 1):
                    start = self.view.text_point(row, col - offset)
                    end = self.view.text_point(row, col)
                    remove = sublime.Region(start, end)
                    self.view.erase(edit, remove)

class SetSplitAtCursorCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        global _split_at

        for region in self.view.sel():
            _, _split_at = self.view.rowcol(region.begin())
            print('SplitPage: split set to col {}'.format(_split_at+1))
