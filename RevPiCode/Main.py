import ModelEstimation
import ProfiBusCom
import Multitasking
import MPC


Run = Multitasking.RunProgram(SecondsDelay=0)

SG = ProfiBusCom.SendAndGet()
ME = ModelEstimation.EstimateModel()

TRS5mpc = MPC.StartMPC()

StartEstimation_trigger = ProfiBusCom.EdgeTrigger()

y = 0
u = 0
good = True;
watchdog = True

while True:
 
    #Reciving data from ProfiBus
    x, StartEstimation, StartMPC, SP = SG.ReciveData()

    #If operator has oreder estimation to start
    if StartEstimation and StartEstimation_trigger.rising_edge(StartEstimation):
        ME.StartUp5x(x)
    #If the estimator is alredy started
    elif StartEstimation:
        y = ME.Estimate(x)
        #print(x)
    else:
        y = 0

    if StartMPC and StartEstimation:
        y_array = ME.model.y.copy()
        x_matrix = ME.model.x.copy()
        u, good = TRS5mpc.RunMPC(x_matrix, y_array, SP)


    watchdog = not(watchdog)

    AlarmList = [watchdog, good]

    SG.SendData(y, u, AlarmList)
    


    Run.NextRun(SG, y, u, AlarmList)

 

  