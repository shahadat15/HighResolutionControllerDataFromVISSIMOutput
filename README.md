# HighResolutionControllerDataFromVISSIMOutput

The input of this project is the .ldp file which is an output VISSIM. ldp file contains signal details. This file has been processed to get the high resolution controller data. 

Two outputs  are generated from this code:
1. PhaseDetails.csv: which report the details of Phase start time, end time, duration, and Phase termination details (e.g. Gap-out, min-out, max-out, coordination-termination, etc. )
2. DetectionDetails.csv: which reprots the timestamps of vehicle detection by different detectors. 
