import Colors

# This file contains configs for how gates should be rendered
class Gate_Config_Data:
    # Constructor
    def __init__(self, display_name="Untitled", control_qubit_index=None, control_qubit_enabled=False, color=Colors.gate_default, color_selected=Colors.selected, description="No description available"):
        self.control_qubit_index = control_qubit_index
        self.control_qubit_enabled = control_qubit_enabled
        self.color = color
        self.color_selected = color_selected
        self.display_name = display_name
        self.description = description


# Defines our gates
H = Gate_Config_Data()
H.display_name = "H"

X = Gate_Config_Data()
X.display_name = "X"

Y = Gate_Config_Data()
Y.display_name = "Y"

Z = Gate_Config_Data()
Z.display_name = "Z"