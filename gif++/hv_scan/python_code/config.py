#### Config file for plotting current x hveff for DOUBLE GAP chamber ####

## To simplify, the analysis should be performed on webdcs machine (To create an account go to README file to see the instructions)

# Path to folders with scan files (normally the path will not change if you use a webdcs account)
files_path = '/var/webdcs/HVSCAN/'

# Dictionary with chamber information. Dict key is the chamber name, dict value contains gap name
chambers={'CHAMBER_NAME' : ['BOT_GAP', 'TOP_GAP']} 
# Example: chambers={'KODELD' : ['BOT-005', 'TOP-003']} 

# List with scan numbers
scan_list=["00xxxx"]						

# List with legends
# Normally we put accumulated charge per run but you can put whatever you want.
lenged_list_bot=["bla",]	

lenged_list_top=["bla",]	

# Example: lenged_list_bot=["$3.25\ mC/cm^2$",]	
# lenged_list_top=["$3.27\ mC/cm^2$",]	




