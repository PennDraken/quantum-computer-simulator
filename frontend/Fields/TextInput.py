from pygame_texteditor import TextEditor

class input_box:
    instance_count = 0

    def __init__(self, screen, x, y, width, height, text):
        self.screen = screen
        self.text = text
        self.obj = TextEditor(offset_x=x, offset_y=y, editor_width=width, editor_height=height, screen=screen)
        self.obj.set_text_from_list(self.text)


    def update(self, tab_panel_y, tab_height):
        self.obj.editor_offset_y = (tab_panel_y + tab_height) + 10
        self.obj.line_start_y = self.obj.editor_offset_y
        self.obj.line_numbers_y = self.obj.editor_offset_y
        self.obj.editor_offset_x = 0
        self.obj.editor_width = self.screen.get_width()
        self.obj.editor_height = self.screen.get_height() - self.obj.editor_offset_y  #can adjust it so it be as long as a vertical list of gates


    def handle_event(self, event, pressed_keys, mouse_x, mouse_y, mouse_pressed):
        self.obj.showable_line_numbers_in_editor = len(self.obj.get_text_as_list()) # how many items/gates are visiable in one scroll page this can be adjusted depedning on how many gates are present
        self.obj.set_colorscheme("dark")
        self.obj.set_cursor_mode("blinking")
        self.obj.display_editor(event, pressed_keys, mouse_x, mouse_y, mouse_pressed)
        self.text = self.obj.get_text_as_string()