# Start GUI
- current working directory needs to SIM_MDP_GUI
python3 new_frontend/ConnectedScreens.py

# Convert UI files to Python
pyuic6 input.ui -o output.py
pyuic6 input.ui -o ../generated_ui/output.py

#Files   
- generated_ui: All of the screens we converted to python fiels from pyuic6 command 
- pyqt_ui: All of the ui screens exported from pyqt creator 
- Config.py: Where we store all of our information (dictionarie) to send to backend 
- ConnectedScreens.py: Where the screens are connected and config dictionaries being updated 

### TODO:   
1. IN PROGRESS -- Figure out how to get the images back 
2. DONE for Intersection -- Make sure all of the buttons are properly names in a meaningful way 
3. DONE(kinda) -- Find a way to allow unlimited number of freeway sections in Config.py
4. ALMOST DONE ONLY POP UPS LEFT -- Add and connected remaining screens.
5. Have widgets load values currently in config.py when changing screens. -- (do we need this??????)
6. Split the different screen classes in ConnectedScreens to different files.
7. Save and Load Config.py to and from a saved file. (optional...)
8. IN PROGRESS -- Update Config file when values change for all checkboxes, spinboxes, dropbox, etc..
9. IN PROGRESS -- Figure out how to return to a specific lane # (both freeway and intersection pages)
10. Design and generate popup screens (add vehicle, edit traffic light setting)
### 