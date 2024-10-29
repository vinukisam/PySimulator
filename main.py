'''
***********************************************************************

NOTES FOR STUDEENTS
-------------------
Change this file only when
    1. when creating images to train your AI model
    2. to change change between cloud and edge modules

***********************************************************************
'''

import analytic_module
import conveyor_module

def main():

    # Parameters:
    #   1. isCloud
    #           =True : Uses cloud module
    #           =False: Uses edge module
    analytic = analytic_module.Listener(isCloud=False)

    # Parameters:
    #   1. shouldAnalyzeImg
    #           =True : To analyze the images
    #           =False: To get images for training
    #   2. imgLimit
    #           =Number: Number of images/rows to be stored (use 50 to get images for training)
    conveyor = conveyor_module.Simulation(shouldAnalyzeImg=True, imgLimit=50)

    analytic.start()
    conveyor.start()

if __name__ == "__main__":
    main()