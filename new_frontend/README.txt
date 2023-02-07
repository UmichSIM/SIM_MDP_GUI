# Start GUI 
python3 ConnectedScreens.py

# Convert UI files to Python
pyuic6 input.ui -o output.py

#Files   
- generated_ui: All of the screens we converted to python fiels from pyuic6 command 
- pyqt_ui: All of the ui screens exported from pyqt creator 
- Config.py: Where we store all of our information (dictionarie) to send to backend 
- ConnectedScreens.py: Where the screens are connected and config dictionaries being updated 

### TODO:   
1. Figure out how to get the images back 
2. Make sure all of the buttons are properly names in a meaningful way 
3. Regenerate screens and convert to python files 
4. DONE -- Figure out how to use config so we can reuse screens 
5. DONE -- Devise a way to send information to backend
    - We decided to do global structures (dictionary) for 4 & 5 
6. DONE(kinda) -- Find a way to allow unlimited number of freeway sections in Config.py
7. Fix previously repeated screens to share 1 instans.
8. Add remaining screens.
9. Have widgets load values currently in config.py when changing screens.
10. Split the different screen classes in ConnectedScreens to different files.
11. Save and Load Config.py to and from a saved file.
### 