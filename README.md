# CMS RPC - Analysis code

This repository is used to house cms rpc analysis codes. There are the following analysis code here:

* GIF++ High voltage scans plots:
  * Folder with codes: cms_rpc_analysis/gif++/hv_scan/python_code/
  * Codes:
    * **config.py** -> Config file to set options for running current_hveff.py (Only Double Gap chambers are configured - SO FAR!!)
    * **current_hveff.py** -> Python scripts to produce Current x HFeff (Change config file and do: python current_hveff.py)   
* Argon scans plots:
  * Folder with codes: cms_rpc_analysis/gif++/argon_scan/
  * Codes:
    * **config.py** -> Config file to set options for running argon_scan.py (Only Double Gap chambers are configured - SO FAR!!)
    * **argon_scan.py** -> Python scripts to produce Current x HFeff, fit the curves, calculate resistance, resistivity and HVonset (Change config file and do: python current_hveff.py) 
* Resistivity monitoring:
  * Folder with codes: cms_rpc_analysis/gif++/resistivity_monitoring/
  * Codes:
    * **resistivity_data.csv** -> CSV with data to be read and processed by resistivity_monitoring.ipynb.
    * **resistivity_monitoring.ipynb** -> Python script to be run in a notebook.

* Rate Scan:
  * Folder with codes: cms_rpc_analysis/gif++/rate_scan/

  * Codes:
    * **config_csv_rate.py** -> Config file to provide information to the main code, create_csv_rate.py
    * **create_csv_rate.py** -> Python script to be run in a notebook.
