import analytic_module
import conveyor_module

def main():

    analytic = analytic_module.Listener(isCloud=False)
    conveyor = conveyor_module.Simulation(shouldAnalyzeImg=True)

    analytic.start()
    conveyor.start()

if __name__ == "__main__":
    main()