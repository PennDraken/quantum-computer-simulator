# This is a class that shows the states at various points of the calculation on window
import pygame
import Utilities.Colors as Colors
import UI

class Calculation_Viewer_Window:
    def __init__(self, screen, x: int, y: int, width: int, height: int, systems: []):
        self.screen: pygame.screen = screen
        self.x = x
        self.y = y
        self.circuit_dx = 0
        self.width = width
        self.height = height
        self.systems = systems
        self.str_registers = []
        self.grid_size = UI.grid_size  # Width and height of the underlying grid
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
            for register_index, register in enumerate(system.registers):
                x = self.x + col * self.grid_size + self.circuit_dx
                y = self.y + grid_row * self.grid_size
                
                # TODO precalculate these somehow? (for performance)
                label = register.get_label()
                state_str = register.get_state_str()
                lines = state_str.splitlines()
                
                # Draw the label showing the qubits of the register
                # Change color to yellow if most recent
                if col==len(self.systems)-1:
                    color = Colors.yellow
                else:
                    color = Colors.white

                pygame.draw.rect(self.screen, color, (x, y, self.grid_size, label_height), width=1)
                text(self.screen, label, x + half_grid_size, y + 4, color, self.title_font)

                # Draws the vector state of the register
                for row, line in enumerate(lines):
                    text(self.screen, line, x + half_grid_size, y + label_height + row * text_height, color, self.state_font)
                
                # Draw the grid rectangle showing end of qubit
                pygame.draw.rect(self.screen, color, (x, y, self.grid_size, len(register.qubits) * self.grid_size), width=2)
                
                # Increment grid row based on how many qubits were in register
                grid_row += len(register.qubits)



def text(screen, string, x, y, color, font):
    text_color = pygame.Color(color)
    text_surface = font.render(string, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y + text_surface.get_height()/2)
    screen.blit(text_surface, text_rect)
