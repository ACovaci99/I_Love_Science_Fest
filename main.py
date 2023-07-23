
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../I_Love_Science_Fest/GUI')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../I_Love_Science_Fest/back_end')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../I_Love_Science_Fest/front_end')))

from GUI import gui_utility

gui_utility.GUI_Main_Page()
