import turtle
import pandas
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- NEW LOGIC FOR OUTPUT PATH ---
# This determines the directory where the .exe is running
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle/exe
    application_path = os.path.dirname(sys.executable)
else:
    # If the application is run as a normal .py script
    application_path = os.path.dirname(os.path.abspath(__file__))

# Define the output folder and file path relative to the .exe's location
output_folder = os.path.join(application_path, "cc")
output_csv_path = os.path.join(output_folder, "non_gusse.csv")

# --- SCRIPT CONTINUES ---

# Use resource_path for READING bundled files
map_path = resource_path("map.gif")
country_csv_path = resource_path("country.csv")

# Ensure the persistent output directory exists before writing to it
os.makedirs(output_folder, exist_ok=True)

window=turtle.Screen()
window.setup(788,594)
window.bgpic(map_path)

counter=0
data=pandas.read_csv(country_csv_path)
contrys=data.countrys.to_list()
lis_contry=[]

while len(lis_contry)<15:
    massege=window.textinput(title=f"Countries: {counter}/15", prompt= "خمن مكان الدوله عل الخريطه").title()
    
    if massege in contrys:
        lis_contry.append(massege)
        coordnate_x=data[data.countrys==massege]["x"].item()
        coordnate_y=data[data.countrys==massege]["y"].item()
        
        g=turtle.Turtle()
        g.penup()
        g.hideturtle()
        g.goto(coordnate_x,coordnate_y)
        g.write(massege)
        
        contrys.remove(massege)
        counter+=1
        
        # Use the NEW persistent output path for WRITING the file
        with open(output_csv_path, "+a", encoding='utf-8') as file:
            file.write(f"{massege}\n")
            
    if massege=="Exit":
        break 

window.mainloop()

