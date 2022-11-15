from PyQt5.QtWidgets import *
import edit_section


page_list = []  # type: list[int]


def populate(vec, val, window):
    """
    connected: none
    function: populates page list with val number of edit_section windows
    """
    for i in range(len(vec),val+1):
        new = edit_section.Edit_Section_Window(i,window)
        vec.append(new)

def remove(vec,val):
    """
    connected: none
    function: removes range from 0 to val of edit_section windows from page_list
    """
    
    for i in range(0,val):
        vec.pop()

        
