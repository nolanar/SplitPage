import sublime
import sublime_plugin

class IndentToSplitCommand(sublime_plugin.TextCommand):

    SPLIT_COL = 40

    def run(self, edit):
        for region in self.view.sel():
            text = self.view.find("[^\s]", region.begin())
            begin_row, col = self.view.rowcol(text.begin())
            end_row, _ = self.view.rowcol(region.end())

            if (col < self.SPLIT_COL):                    
                insert_string = " " * (self.SPLIT_COL - col)
                for row in range(begin_row, end_row + 1):
                    insert_point = self.view.text_point(row, col)
                    self.view.insert(edit, insert_point, insert_string)

            elif (col > self.SPLIT_COL):
                offset = col - self.SPLIT_COL
                for row in range(begin_row, end_row + 1):
                    start = self.view.text_point(row, col - offset)
                    end = self.view.text_point(row, col)
                    remove = sublime.Region(start, end)
                    self.view.erase(edit, remove)
