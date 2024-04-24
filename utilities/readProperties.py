#This file reads the common data from ini file - Configurations/config.in
import os
import configparser

# current_directory = os.path.dirname(os.path.abspath(__file__))
#
# # Set the path to the config.ini file
# config_path = os.path.join(current_directory, 'Configurations', 'config.ini')
#
# # Read the config.ini file
# config = configparser.ConfigParser()
# config.read(config_path)

config = configparser.ConfigParser()
config.read("D:\\Git//test-automation\\3DX_pythonProject\\Configurations\\config.ini")

class ReadConfig:
    # for every variable access, need same no of methods
    # static method, so that this method can be invokled using classname
    @staticmethod
    def getURL():
        url = config.get('common info', 'baseURL')
        return url

    @staticmethod
    def getUsername():
        username = config.get('common info', 'username')
        return username

    @staticmethod
    def getPassword():
        password = config.get('common info', 'password')
        return password

    @staticmethod
    def getdocument_Reg():
        document_Reg = config.get('common info', 'document_Reg')
        return document_Reg

    @staticmethod
    def getdashboard_name():
        dashboard_Name = config.get('common info', 'dashboard_name')
        return dashboard_Name

    @staticmethod
    def getdwidget_name():
        widget_name = config.get('common info', 'widget_name')
        return widget_name

# print(ReadConfig.getURL())