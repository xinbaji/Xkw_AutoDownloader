import logging
import os
class Log:
    def __init__(self,log_name,mode:str = 'i') -> None:
        log_level = logging.DEBUG if mode == 'd' else logging.INFO
        if not os.path.exists("./log/log.txt"):
            os.makedirs('log',exist_ok=True)
            with open("./log/log.txt","w") as f:
                f.write("日志生成成功！")
                f.write("\n")
                f.close()
        handler = logging.FileHandler("./log/log.txt")
        handler.setLevel(level = log_level)
        formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        console = logging.StreamHandler()
        console.setLevel(log_level)
        
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(level = log_level)
        self.logger.addHandler(handler)
        self.logger.addHandler(console)
    
    def debug(self,message):
        self.logger.debug(message)
        
    def info(self,message):
        self.logger.info(message)
        
    def warning(self,message):
        self.logger.warning(message)
        
    def error(self,message):
        self.logger.error(message,exc_info = True)
        
    
        
        