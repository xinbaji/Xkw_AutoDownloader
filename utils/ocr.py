import ddddocr
from utils.log import Log
class Ocr:
    def __init__(self) -> None:
        
        self.ocr= ddddocr.DdddOcr()
        self.log=Log('ocr','d')
    def ocr_verifycode(self,picpath = "./img/needocr.png"):
        image = open(picpath, "rb").read()
        result = self.ocr.classification(image)
        self.log.debug("result:"+str(result))
        
        if len(result) != 4:
            self.log.info("未识别到结果，重新检测")
            return False
        
        for i in result:
            if not i.isdigit() :
                self.log.info("未识别到结果，重新检测")
                return False
        
        code=str(result)
        self.log.info("当前验证码为："+code)
        
        return code
    