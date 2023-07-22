
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ILSF/GUI')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ILSF/back_end')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ILSF/front_end')))

from GUI import gui_utility

gui_utility.GUI_Main_Page()
