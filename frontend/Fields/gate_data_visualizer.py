import pygame
import numpy as np
import Utilities.Colors as Colors
import UI

# Visualizes the matrix of a given gate
class Matrix_Window():
    def __init__(self, screen):
        self.matrix=[]
        # self.matrix_string=self.set_matrix(matrix)
        self.active=False
        self.screen=screen

    def draw(self):
        # Create a string for the matrix
        pygame.draw.rect(self.screen, Colors.black, (self.screen.get_rect()))
        UI.text_multiline(self.screen, self.matrix_string, 0, 0, Colors.white)
        pass

    def update(self):
        pass
    
    # Takes a np.array matrix and transforms it into a string
    def set_matrix(self, matrix : np.array):
        matrix_string = ""
        spacing = 20  # Distance between each number (number centered every 8 characters)
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                num = matrix[i][j]
                real = round(num.real, 2)
                imag = round(num.imag, 2)
                formatted_num = f"{real} + {imag}j"  # Format real and imaginary parts
                padding = spacing - len(formatted_num)
                if padding % 2 == 0:
                    left_padding = right_padding = padding // 2
                else:
                    left_padding = padding // 2 + 1
                    right_padding = padding // 2
                matrix_string += " " * left_padding + formatted_num + " " * right_padding
            matrix_string += "\n"  # Add newline after each row
        self.matrix_string = matrix_string
        print(matrix_string)
        return matrix_string

# Example usage
# matrix = np.array([[1+2j, 3+4j], [5+6j, 7+8j]])
# window = Matrix_Window(matrix)
# print(window.matrix_string)