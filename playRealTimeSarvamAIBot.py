#####################################################
#### Written By: SATYAKI DE                      ####
#### Written On: 20-Aug-2024                     ####
#### Modified On 30-Aug-2024                     ####
####                                             ####
#### Objective: This is the main calling         ####
#### python script that will invoke the          ####
#### clsSarvamAI class to initiate the           ####
#### Indic language-bot in real-time.            ####
####                                             ####
#####################################################

# We keep the setup code in a different class as shown below.
import clsSarvamAI as sai
from clsConfigClient import clsConfigClient as cf

import datetime
import logging

def main():
    try:
        # Other useful variables
        debugInd = 'Y'

        var = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('Start Time: ', str(var))

        # Initiating Log Class
        general_log_path = str(cf.conf['LOG_PATH'])

        # Enabling Logging Info
        logging.basicConfig(filename=general_log_path + 'genSarvamAILog.log', level=logging.INFO)

        print('Started Sarvam AI Optimized Assitant with Indic Languages!')

        # Passing source data csv file
        x1 = sai.clsSarvamAI()

        r1 = x1.realTimeTranslation()

        if (r1 == 0):
            print('Successfully Exited the Application!')
        else:
            print('Failed to exit!')

        var2 = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        print('End Time: ', str(var2))

    except Exception as e:
        x = str(e)
        print('Error: ', x)

if __name__ == "__main__":
    main()
