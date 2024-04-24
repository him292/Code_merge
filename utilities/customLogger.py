import logging

# class LogGen:
#     @staticmethod
#     def loggen():
#         logging.basicConfig(filename=".\\Logs\\automation.log",
#                             format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%y %I:%M:%S: %p')
#         logger = logging.getLogger()
#         logger.setLevel(logging.INFO)
#         return logger
class LogGen:
    # we added the static method so that we dont need to use the "self" keyword in the below fucntion
    @staticmethod
    # now create one object for logging
    def loggen():
        logger = logging.getLogger()
        # below file name is the path where you want to generate the logs
        fhandler = logging.FileHandler(filename='D:\\Git\\test-automation\\feature\\Code_merge\\Logs\\automation.log', mode='a')
        # then the timestamp format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fhandler.setFormatter(formatter)
        logger.addHandler(fhandler)
        # set level is to set the level of log like WARNING, INFO or ERROR
        logger.setLevel(logging.INFO)
        return logger