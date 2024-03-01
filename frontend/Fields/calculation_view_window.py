# This is a class that shows the states at various points of the calculation on window
import pygame
import Utilities.Colors as Colors
import time

class Calculation_Viewer_Window:
    def __init__(self, screen, x: int, y: int, width: int, height: int, systems: []):
        self.screen: pygame.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.systems = systems
        self.str_registers = []
        self.grid_size = 90  # Width and height of the underlying grid
        self.precompute_register_info()
        self.title_font = pygame.font.Font(None, 24)
        self.state_font = pygame.font.Font(None, 20)

    def precompute_register_info(self):
        for system in self.systems:
            for register in system.registers:
                label = register.get_label()
                state_str = register.get_state_str()
                lines = state_str.splitlines()  # Precompute here
                self.str_registers.append((label, lines))  # Store lines instead of state_str

    def draw(self):
        # Precompute values
        half_grid_size = self.grid_size / 2
        label_height = 30
        text_height = 20
        

        for col, system in enumerate(self.systems):
            grid_row = 0
            num_registers = len(system.registers)
            str_registers = self.str_registers[col * num_registers: (col + 1) * num_registers]
            col_grid_size = self.x + col * self.grid_size
            for register_index, (label, lines) in enumerate(str_registers):  # Retrieve lines instead of state_str
                x = col_grid_size
                y = grid_row * self.grid_size + self.y
                
                # Draw the label showing the qubits of the register
                pygame.draw.rect(self.screen, Colors.white, (x, y, self.grid_size, label_height), width=1)  # Box around text
                text(self.screen, label, x + half_grid_size, y, Colors.white, self.title_font)

                # Draws the vector state of the register
                for row, line in enumerate(lines):  # Iterate over precomputed lines
                    text(self.screen, line, x + half_grid_size, y + label_height + row * text_height, Colors.white, self.state_font)
                
                # Draw the grid rectangle showing end of qubit
                pygame.draw.rect(self.screen, Colors.white, (x, y, self.grid_size, len(system.registers[register_index].qubits) * self.grid_size), width=2)
                
                # Increment grid row based on how many qubits were in register
                grid_row += len(system.registers[register_index].qubits)


def text(screen, string, x, y, color, font):
    text_color = pygame.Color(color)
    text_surface = font.render(string, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y + text_surface.get_height()/2)
    screen.blit(text_surface, text_rect)
