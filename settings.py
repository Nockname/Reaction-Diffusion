import numpy as np

class Settings:
    @staticmethod
    def __chooseCustom(settingName, resultType):

        while True:
            userInput = input("Custom value for the {}: ".format(settingName))

            try:
                if resultType == "int":
                    return int(userInput)
                if resultType == "float":
                    return float(userInput)
                if resultType == "str":
                    return str(userInput)

            except ValueError:
                print("The input does not match the desired type. Please supply a {} input".format(resultType))

    @staticmethod
    def __chooseOneSetting(settingName, options, resultType):

        print("Pick the number corresponding to the desired preset for the {}. Enter 0 to input a custom value".format(settingName))
        for i in range(len(options)):
            print("\t{}) {}".format(i+1, options[i]))

        if resultType != "bool":
            print("\t0) Custom")

        while True:
            try:
                userInput = int(input("Selector: "))
            except ValueError:
                print("Please supply an integer output between 0 and {}".format(len(options)))
                continue

            if userInput == 0 and resultType != "bool":
                return Settings.__chooseCustom(settingName, resultType)

            if userInput >= 1 and userInput <= len(options):
                return options[userInput-1]

            if resultType != "bool":
                print("Please supply an integer output between 0 and {}".format(len(options)))
            else:
                print("Please supply an integer output between 1 and {}".format(len(options)))

    @staticmethod
    def __chooseTwoSettings(setting1Name, setting2Name, options, resultType):
        print("Pick the number corresponding to the desired preset for {} and {}. Enter 0 to input a custom value".format(setting1Name, setting2Name))
        for i in range( len (options) ):
            print("\t{}) {} and {}".format(i+1, options[i][0], options[i][1]))

        print("\t0) Custom")

        while True:
            try:
                userInput = int(input("Selector: "))
            except ValueError:
                print("Please supply an integer output between 0 and {}".format(len(options)))
                continue

            if userInput == 0:
                result1 = Settings.__chooseCustom(setting1Name, resultType)
                result2 = Settings.__chooseCustom(setting2Name, resultType)
                return result1, result2

            if userInput >= 1 and userInput <= len(resultType):
                result1 = options[userInput-1][0]
                result2 = options[userInput-1][1]
                return result1, result2

            print("Please supply an integer output between 0 and {}".format(len(options)))

    @staticmethod
    def chooseAllSettings():

        #HEIGHT AND WIDTH
        heightAndWidthValues = [[150, 150], [500, 500], [1000, 1000]]
        HEIGHT, WIDTH = Settings.__chooseTwoSettings("height", "width", heightAndWidthValues, "int")

        #FRAMES AND FPS
        framesAndFPSValues = [[300, 10], [1000, 30], [3000, 60]]
        FRAMES, FPS = Settings.__chooseTwoSettings("frames", "FPS", framesAndFPSValues, "int")

        feedStartAndEndValues = [[0.001, 0.01], [0.001, 0.02], [0.001, 0.05]]
        FEEDSTART, FEEDEND = Settings.__chooseTwoSettings("smallest feed value", "biggest feed value", feedStartAndEndValues, "float")

        killStartAndEndValues = [[0.01, 0.08], [0.03, 0.06], [0.04, 0.05]]
        KILLSTART, KILLEND = Settings.__chooseTwoSettings("smallest kill value", "biggest kill value", killStartAndEndValues, "float")

        CREATE_VIDEO = Settings.__chooseOneSetting("Create Video", [True, False], "bool")

        return HEIGHT, WIDTH, FRAMES, FPS, FEEDSTART, FEEDEND, KILLSTART, KILLEND, CREATE_VIDEO

HEIGHT, WIDTH, FRAMES, FPS, FEEDSTART, FEEDEND, KILLSTART, KILLEND, CREATE_VIDEO = Settings.chooseAllSettings()

FEEDRATE=np.linspace(FEEDSTART, FEEDEND, WIDTH, endpoint=True)
KILLRATE=np.linspace(KILLSTART, KILLEND, HEIGHT, endpoint=True)

TIMESCALE=1
START_SEPARATION=50
START_WIDTH=5

CONVERT_METHOD="linear"
MIN_COLOR=[0, 0, 0, 255]
MAX_COLOR=[255, 255, 255, 255]
COLORWHEEL=MAX_COLOR+MIN_COLOR

ADIFFUSE=1
BDIFFUSE=0.5

VIDEO_NAME="diffusion"
