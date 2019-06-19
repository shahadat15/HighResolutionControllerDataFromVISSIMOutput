import pandas as pd
from pathlib import Path


########### User Input ###################
input_file_name = "C:/Users/miqba005/OneDrive - Florida International University/Shahadat/HRCD conversion/Main Model_2076_163.ldp"
output_file_location = "C:/Users/miqba005/OneDrive - Florida International University/Shahadat/HRCD conversion/"
file_column_names = ["ActivePhase1","ActivePhase4","ActivePhase3","ActivePhase2","Yellow1","Yellow2","Yellow3","Yellow4","Walk1","Walk2","Walk3","Walk4",
              "VehicleExtension1","VehicleExtension2","VehicleExtension3","VehicleExtension4","SimulSecond","RedClearance1","RedClearance2","RedClearance3","RedClearance4",
              "PedClearance1","PedClearance2","PedClearance3","PedClearance4","MinGreen1","MinGreen2","MinGreen3","MinGreen4","MinDwell","MaxGreen1","MaxGreen2","MaxGreen3","MaxGreen4",
              "MaxDwell","GapinEffect1","GapinEffect2","GapinEffect3","GapinEffect4","CycleTime","Cyclesecond",
              "CPDetector1","CPDetector2","CPDetector3","CPDetector4","CPDetector5","CPDetector6","CPDetector7","CPDetector8",
              "CoordinationSplit1","CoordinationSplit2","CoordinationSplit3","CoordinationSplit4","AddedInitial1","AddedInitial2","AddedInitial3","AddedInitial4"]


######### Main Analysis ###############

### Read the file and preprocess the data ######
file2 = open("C:/Users/miqba005/OneDrive - Florida International University/Shahadat/HRCD conversion/Main Model_2076_163.ldp", "r")
temp_dataframe = []
i=0
for line in file2:
    if i < 29:
        i += 1
    else:
        words = line.split()
        temp_dataframe.append(words)
file2.close()
InputFile = pd.DataFrame(temp_dataframe)
InputFile.columns = file_column_names
InputFile = InputFile[["ActivePhase1","ActivePhase2","Yellow1","Yellow2","Walk1","Walk2",
              "VehicleExtension1","VehicleExtension2","SimulSecond","RedClearance1","RedClearance2",
              "PedClearance1","PedClearance2","MinGreen1","MinGreen2","MaxGreen1","MaxGreen2",
              "GapinEffect1","GapinEffect2","CycleTime","Cyclesecond",
              "CoordinationSplit1","CoordinationSplit2"]]
InputFile['SimulSecond'] = InputFile['SimulSecond'].str[:-9].astype(float)
InputFile.ActivePhase1 = InputFile.ActivePhase1.astype(int)
InputFile.Yellow1 = InputFile.Yellow1.astype(int)
InputFile.RedClearance1 = InputFile.RedClearance1.astype(int)
InputFile.MaxGreen1 = InputFile.MaxGreen1.astype(int)
InputFile.CoordinationSplit1 = InputFile.CoordinationSplit1.astype(int)
InputFile.ActivePhase1 = InputFile.ActivePhase1.astype(int)
InputFile.ActivePhase2 = InputFile.ActivePhase2.astype(int)

### initiate the output files ###########
output_data = pd.DataFrame(columns=["Phase","StartTime","EndTime","Duration","Phase_termination_details"])
output_data_extension = pd.DataFrame(columns=["Phase","Detection_time"])

### Run the analysis for ring 1
active_phase = 0
temp_rows = pd.DataFrame(columns=InputFile.columns)
ModifiedData = InputFile.loc[InputFile["Yellow1"] == 0]
ModifiedData = ModifiedData.loc[ModifiedData["RedClearance1"] == 0]
ModifiedData = ModifiedData.loc[ModifiedData["ActivePhase1"] > 0]
for row in ModifiedData.iterrows():
    if (row[1][0] == 1) & (row[1][6] == 15):
        output_data_extension.loc[len(output_data_extension)] = [int(row[1][0]),float(row[1][8])]
    elif (row[1][0] == 2) & (row[1][6] == 30):
        output_data_extension.loc[len(output_data_extension)] = [int(row[1][0]),float(row[1][8])]
    elif (row[1][0] == 3) & (row[1][6] == 20):
        output_data_extension.loc[len(output_data_extension)] = [int(row[1][0]), float(row[1][8])]
    elif (row[1][0] == 4) & (row[1][6] == 20):
        output_data_extension.loc[len(output_data_extension)] = [int(row[1][0]), float(row[1][8])]

    if active_phase == row[1][0]:
        temp_rows = temp_rows.append(row[1])
    elif len(temp_rows)>1:
        analysis_Lastrow = temp_rows.iloc[-1:]
        analysis_Firstrow = temp_rows.iloc[:1]
        if (int(analysis_Lastrow.MaxGreen1) == 1):
            output_data.loc[len(output_data)] = [int(analysis_Lastrow.ActivePhase1),
                                                 float(analysis_Firstrow.SimulSecond),
                                                 float(analysis_Lastrow.SimulSecond), (
                                                         float(analysis_Lastrow.SimulSecond) - float(
                                                     analysis_Firstrow.SimulSecond)), "MaxOut"]
        elif (int(analysis_Lastrow.MinGreen1) == 1):
            output_data.loc[len(output_data)] = [int(analysis_Lastrow.ActivePhase1),
                                                 float(analysis_Firstrow.SimulSecond),
                                                 float(analysis_Lastrow.SimulSecond), (
                                                         float(analysis_Lastrow.SimulSecond) - float(
                                                     analysis_Firstrow.SimulSecond)), "MinOut"]
        elif (int(analysis_Lastrow.CoordinationSplit1) == 1):
            output_data.loc[len(output_data)] = [int(analysis_Lastrow.ActivePhase1),
                                                 float(analysis_Firstrow.SimulSecond),
                                                 float(analysis_Lastrow.SimulSecond), (
                                                         float(analysis_Lastrow.SimulSecond) - float(
                                                     analysis_Firstrow.SimulSecond)), "CoordinationTimeOut"]
        elif (int(analysis_Lastrow.VehicleExtension1) == 1):
            output_data.loc[len(output_data)] = [int(analysis_Lastrow.ActivePhase1),
                                                 float(analysis_Firstrow.SimulSecond),
                                                 float(analysis_Lastrow.SimulSecond), (
                                                         float(analysis_Lastrow.SimulSecond) - float(
                                                     analysis_Firstrow.SimulSecond)), "GapOut"]
        else:
            output_data.loc[len(output_data)] = [int(analysis_Lastrow.ActivePhase1),
                                                 float(analysis_Firstrow.SimulSecond),
                                                 float(analysis_Lastrow.SimulSecond), (
                                                         float(analysis_Lastrow.SimulSecond) - float(
                                                     analysis_Firstrow.SimulSecond)), "Other"]
        active_phase = row[1][0]
        temp_rows = pd.DataFrame(columns=InputFile.columns)
        temp_rows = temp_rows.append(row[1])
    else:
        active_phase = row[1][0]
        temp_rows = pd.DataFrame(columns=InputFile.columns)
        temp_rows = temp_rows.append(row[1])


### Run the analysis for ring 2
active_phase = 0
temp_rows = pd.DataFrame(columns=InputFile.columns)
ModifiedData = InputFile.loc[InputFile["Yellow2"] == 0]
ModifiedData = ModifiedData.loc[ModifiedData["RedClearance2"] == 0]
ModifiedData = ModifiedData.loc[ModifiedData["ActivePhase2"] > 0]
for row in ModifiedData.iterrows():
    if (row[1][1] == 1) & (row[1][6] == 15):
        output_data_extension.loc[len(output_data_extension)] = [int(row[1][1]),float(row[1][8])]
    elif (row[1][1] == 6) & (row[1][6] == 30):
        output_data_extension.loc[len(output_data_extension)] = [int(row[1][1]),float(row[1][8])]
    elif (row[1][1] == 5) & (row[1][6] == 15):
        output_data_extension.loc[len(output_data_extension)] = [int(row[1][1]),float(row[1][8])]

    if active_phase == row[1][1]:
        temp_rows = temp_rows.append(row[1])
    elif (len(temp_rows)>1):
        analysis_Lastrow = temp_rows.iloc[-1:]
        analysis_Firstrow = temp_rows.iloc[:1]
        if (int(analysis_Lastrow.MaxGreen2) == 1):
            output_data.loc[len(output_data)] = [int(analysis_Lastrow.ActivePhase2),
                                                 float(analysis_Firstrow.SimulSecond),
                                                 float(analysis_Lastrow.SimulSecond), (
                                                         float(analysis_Lastrow.SimulSecond) - float(
                                                     analysis_Firstrow.SimulSecond)), "MaxOut"]
        elif (int(analysis_Lastrow.MinGreen2) == 1):
            output_data.loc[len(output_data)] = [int(analysis_Lastrow.ActivePhase2),
                                                 float(analysis_Firstrow.SimulSecond),
                                                 float(analysis_Lastrow.SimulSecond), (
                                                         float(analysis_Lastrow.SimulSecond) - float(
                                                     analysis_Firstrow.SimulSecond)), "MinOut"]
        elif (int(analysis_Lastrow.CoordinationSplit2) == 1):
            output_data.loc[len(output_data)] = [int(analysis_Lastrow.ActivePhase2),
                                                 float(analysis_Firstrow.SimulSecond),
                                                 float(analysis_Lastrow.SimulSecond), (
                                                         float(analysis_Lastrow.SimulSecond) - float(
                                                     analysis_Firstrow.SimulSecond)), "CoordinationTimeOut"]

        elif (int(analysis_Lastrow.VehicleExtension2) == 1):
            output_data.loc[len(output_data)] = [int(analysis_Lastrow.ActivePhase2),
                                                 float(analysis_Firstrow.SimulSecond),
                                                 float(analysis_Lastrow.SimulSecond), (
                                                         float(analysis_Lastrow.SimulSecond) - float(
                                                     analysis_Firstrow.SimulSecond)), "GapOut"]
        else:
            output_data.loc[len(output_data)] = [int(analysis_Lastrow.ActivePhase2),
                                                 float(analysis_Firstrow.SimulSecond),
                                                 float(analysis_Lastrow.SimulSecond), (
                                                         float(analysis_Lastrow.SimulSecond) - float(
                                                     analysis_Firstrow.SimulSecond)), "Other"]
        active_phase = row[1][1]
        temp_rows = pd.DataFrame(columns=InputFile.columns)
        temp_rows = temp_rows.append(row[1])
    else:
        active_phase = row[1][1]
        temp_rows = pd.DataFrame(columns=InputFile.columns)
        temp_rows = temp_rows.append(row[1])


##### Write files
output_data.to_csv(Path(output_file_location+'PhaseDetails.csv'),index = False)
output_data_extension.Phase = output_data_extension.Phase.astype(int)
output_data_extension.to_csv(Path(output_file_location+'DetectionDetails.csv'),index = False)

###################### END ##################################


