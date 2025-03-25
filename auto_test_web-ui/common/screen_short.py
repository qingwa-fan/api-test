import os
import allure
import pyscreenshot as ImageGrab
import time

currTime = time.strftime("%m%d%H%M%S")
def getScreenShot(funcName):
    filename = os.path.abspath(os.path.join(os.getcwd(), ".")) + r'/Screen_shot/' + funcName+' ' + currTime + '.png'
    im = ImageGrab.grab()
    im.save(filename)
    im.close()
    allure.attach.file(source=filename, name=f'{funcName}+{currTime}', attachment_type=allure.attachment_type.PNG)