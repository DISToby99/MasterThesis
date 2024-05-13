import ModelEstimation
import ProfiBusCom
import Sleep1m
import MPC

#Creating classes
Run = Sleep1m.RunProgram(SecondsDelay=0)

SG = ProfiBusCom.SendAndGet()
ME = ModelEstimation.EstimateModel()

TRS5mpc = MPC.StartMPC()

StartEstimation_trigger = ProfiBusCom.EdgeTrigger()

KF = ModelEstimation.KalmanFilter()

#Initial values
y = 0
u = 0
good = True
watchdog = True

x2_last = 6

while True:
 
    #Reciving data from ProfiBus
    x, StartEstimation, StartMPC, SP, y_meas, Use_meas = SG.ReciveData()

    #If PLC has oredered estimation to start
    if StartEstimation and StartEstimation_trigger.rising_edge(StartEstimation):
        ME.StartUp5x(x)
    #If the estimator is alredy started
    elif StartEstimation:
        y = ME.Estimate(x)

        #If theer has been a a big change in Q_in start estimation all over again        
        if abs(x2_last - x[1]) > 1:
            y = SP
        ME.model.NewSampleInY(y)

    else:
        y = 0
        ME.model.y[9] = SP

    #If MPC is started from PLC
    if StartMPC and StartEstimation:
        #Gets the x and y matrix from model
        y_array = ME.model.y.copy()
        x_matrix = ME.model.x.copy()
        #calaculates new setpoint
        u, good = TRS5mpc.RunMPC(x_matrix, y_array, SP)
    else:
        u = 0
        good = True
        TRS5mpc.MPC.U = x[3]

    #Changing the watchdog state
    watchdog = not(watchdog)

    #Creating a list of boolian values of alarms to send to PLC
    AlarmList = [watchdog, good]

    #Sedning all data to PLC
    SG.SendData(y, u, AlarmList)
    
    x2_last = x[1]
    
    #Sleeping until next minute
    Run.NextRun(SG, y, u, AlarmList)

 

  
