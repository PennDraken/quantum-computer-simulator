import sys
import os
from math import floor
import copy
import re
import pygame
import json
# Change path (in order to import backend module)
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

# Custom modules
import screenHandler
import UI
import Utilities.Colors as Colors
import frontend.q_sphere as q_sphere
import Fields.MenuButton as MenuGateButton
import Fields.calculation_view_window as calculation_view_window
import Fields.qubit_name_panel as qubit_name_panel
from backend.circuit import Circuit
from backend.Gates import string_to_gate
import backend.algorithms as algorithms # This is used to quickly set starting circuit state
from frontend.Fields.circuit_navigation_panel import Circuit_Navigation_Window
import gates
from gates import Gate, gateHandler
from Utilities.mouse import Mouse
import Fields.TextInput as input_box
import Fields.gate_date_visualizer as gate_data_visualizer
from tkinter.filedialog import asksaveasfile, askopenfile
from time import time
screen = screenHandler.screen
gate_handler : gateHandler = gateHandler()
framerate = pygame.time.Clock()

circuit : Circuit = Circuit(algorithms.shor_subroutine_circuit(7,15))
circuit.run()