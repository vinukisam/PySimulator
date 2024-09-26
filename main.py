import analytic_module
import conveyor_module

def main():
    cloud_endPointUrl = "https://cookietest-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/b690e8e3-f829-4219-98bf-f8b00f79abb3/detect/iterations/Iteration1/image"
    local_endPointUrl = "http://localhost:5000/image"
    apiKey = "83cbb48fe107400c818014b9c892e08b"

    analytic = analytic_module.Listener(local_endPointUrl, apiKey)
    conveyor = conveyor_module.Simulation(True)

    analytic.start()
    conveyor.start()

if __name__ == "__main__":
    main()