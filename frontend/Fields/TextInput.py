from pygame_texteditor import TextEditor
import pygame

class input_box:

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
        self.obj.editor_height = self.screen.get_height() - self.obj.editor_offset_y  # can adjust it so it be as long as a vertical list of gates

    def handle_event(self, event, pressed_keys, mouse_x, mouse_y, mouse_pressed):
        self.obj.showable_line_numbers_in_editor = self.obj.editor_height // 19  # len(self.obj.get_text_as_list()) # how many items/gates are visiable in one scroll page this can be adjusted depedning on how many gates are present
        # self.obj.set_colorscheme("dark")
        # self.obj.set_cursor_mode("blinking")
        self.obj.display_editor(event, pressed_keys, mouse_x, mouse_y, mouse_pressed)
        self.text = self.obj.get_text_as_string()

class Button():
    def __init__(self, screen, color_base, color_selected, buttons: [str], input_box_instance:input_box):
        self.screen = screen
        self.rect = [pygame.Rect(0, 0, 0, 0) for _ in buttons]
        self.text = buttons
        self.color = [color_base for _ in buttons]  # Color thatds drawn
        self.color_unselected = color_base
        self.color_selected = color_selected
        self.selected = [False for _ in buttons]
        self.height = 40
        self.input_box_instance = input_box_instance

    def draw(self):
        border = 5
        for i in range(0, len(self.text)):
            outline_rect = self.rect[i].inflate(border * 2, border * 2)  # Make a larger rect for the outline
            pygame.draw.rect(self.screen, (0, 0, 0), outline_rect)
            pygame.draw.rect(self.screen, self.color[i], self.rect[i])

            text(self.screen, self.text[i], self.rect[i].x + self.rect[i].width / 2,
                 self.rect[i].y + self.rect[i].height / 2, (0, 0, 0))

    def update(self, x, y, width=100, height=40):
        x -= 115
        y += 25
        margin = 20
        for i in range(0, len(self.text)):
            self.rect[i].x = x
            self.rect[i].y = y + (i*(height+margin))
            self.rect[i].width = width
            self.rect[i].height = height


    def handle_event(self, mouse_x, mouse_y, mouse_pressed,gates_cleaned) -> str:
        for i, rect in enumerate(self.rect):
            if rect.collidepoint(mouse_x, mouse_y):
                if mouse_pressed[0]:
                    self.selected[i] = True
                    self.color[i] = self.color_selected
                    if self.text[i] == "UPDATE":
                        self.input_box_instance.text = gates_cleaned
                        self.input_box_instance.obj.set_text_from_list(self.input_box_instance.text)
                    else:
                        return self.text[i]
                else:
                    self.selected[i] = not self.selected[i]
                    self.color[i] = self.color_unselected

""""    def button_function(self, button: str, gate_screen : [str], gate_text : [str]):
        match button:
            case "UPDATE":
                self.input_box_instance.text = gate_screen
            case "SUBMIT":"""""



def text(screen, string, x, y, color):
    font = pygame.font.Font(None, 24)
    text_color = pygame.Color(color)
    text_surface = font.render(string, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
