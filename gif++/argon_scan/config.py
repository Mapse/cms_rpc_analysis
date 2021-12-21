#### Config file argon scan for DOUBLE GAP chamber ####

## To simplify, the analysis should be performed on webdcs machine (To create an account go to README file to see the instructions)

# Path to folders with scan files (normally the path will not change if you use a webdcs account)
files_path = '/var/webdcs/HVSCAN/'

# Dictionary with chamber information. Dict key is the chamber name, dict value contains another dict with gap information
#
chambers={'DEMO-RE3-1-Ghent-186' : {'TOP' : 14000, 'BOT' : 14000}}
# Example: chambers={'KODELD' : ['BOT-005', 'TOP-003']} 

# Electrode tickness
thick = 0.14 #cm^2

# String with scan numbers
scan_id="000266"						

## Fit parameters

# Ranges depends on where the curve starts to increase

# range 1
# Normally low value is close to the HV value which
# the plot starts to increase
range_gr1 = [1580, 3000]

# range 2
range_gr2 = [1380, 3000]

# Fit start 
HV_start = 1570

# Unknown value
parameter = 3000
