################################################
#### Written By: SATYAKI DE                 ####
#### Written On:  15-May-2020               ####
#### Modified On: 30-Aug-2024               ####
####                                        ####
#### Objective: This script is a config     ####
#### file, contains all the keys for        ####
#### personal Sarvam AI's LLM evaluation    ####
#### solution to fetch the KPIs to tune it. ####
####                                        ####
################################################

import os
import platform as pl

class clsConfigClient(object):
    Curr_Path = os.path.dirname(os.path.realpath(__file__))

    os_det = pl.system()
    if os_det == "Windows":
        sep = '\\'
    else:
        sep = '/'

    conf = {
        'APP_ID': 1,
        'ARCH_DIR': Curr_Path + sep + 'arch' + sep,
        'PROFILE_PATH': Curr_Path + sep + 'profile' + sep,
        'LOG_PATH': Curr_Path + sep + 'log' + sep,
        'DATA_PATH': Curr_Path + sep + 'data' + sep,
        'OUTPUT_PATH': Curr_Path + sep + 'output' + sep,
        'TEMP_PATH': Curr_Path + sep + 'temp' + sep,
        'IMAGE_PATH': Curr_Path + sep + 'Image' + sep,
        'AUDIO_PATH': Curr_Path + sep + 'audio' + sep,
        'SESSION_PATH': Curr_Path + sep + 'my-app' + sep + 'src' + sep + 'session' + sep,
        'JSONFileNameWithPath': Curr_Path + sep + 'GUI_Config' + sep + 'CircuitConfiguration.json',
        'OUTPUT_DIR': 'model',
        'APP_DESC_1': 'NASA Demo!',
        'DEBUG_IND': 'Y',
        'INIT_PATH': Curr_Path,
        'SARVAM_AI_KEY': "80JSHSD&&-JSU7-89Hu-Jh90-**hjdhYU8",
        'MODEL_1': "bulbul:v1",
        'MODEL_2': "saaras:v1",
        'MODEL_3': "mayura:v1",
        "appType":"application/json",
        "conType":"keep-alive",
        "CACHE":"no-cache",
        "MAX_RETRY": 3,
        'BASE_URL': "https://api.sarvam.ai/",
        'TITLE': "Sarvam AI Demo!",
        'TEMP_VAL': 0.2,
        'PATH' : Curr_Path,
        'MAX_TOKEN' : 512,
        'MAX_CNT' : 5,
        'OUT_DIR': 'data',
        'OUTPUT_DIR': 'output',
        'AUDIO_FILE': 'srcFile.wav',
        'BENGALI_CD': "bn-IN",
        'ENGLISH_CD': "en-IN",
        'SPKR_NAME': "amol",
        'SPKR_GNDR': "Male",
        'FUNC_1': 'speech-to-text-translate',
        'FUNC_2': 'translate',
        'FUNC_3': 'text-to-speech',
        'CLEANED_FILE': 'cleanedFile.csv',
        'CLEANED_FILE_SHORT': 'cleanedFileMod.csv',
        'SUBDIR_OUT': 'output',
        'SESSION_CACHE_FILE': 'sessionCacheCounter.csv',
        'IMAGE_FILE': 'earth.jpeg',
        'CACHE_FILE': 'data.pkl',
        'ADMIN_KEY': "Admin@23",
        'SECRET_KEY': "Adsec@23",
        "limRec": 50,
        "USER_NM": "Test",
        "USER_PWD": "Test@23",
        "DB_PATH": Curr_Path + sep + 'data' + sep
    }
