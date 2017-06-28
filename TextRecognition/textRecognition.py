########################################
# title: Detect Markers                #
# version: 1.0                         #
# author: Magdalena Peplowska          #
# thanks to pytesseract library        #
# screens of GUI in GUI_screens folder #
########################################

import sys
import cv2
import PIL
from PIL import Image
from PyQt4 import QtGui, QtCore
import numpy as np
import pytesseract


class GUI(QtGui.QMainWindow):

    def __init__(self):
        super(GUI, self).__init__()
        self.initUI()
        self.recognition = ImageRecognition()     

       
    def initUI(self):     
        btnLoad = QtGui.QPushButton('Load image', self)
        btnLoad.resize(100, 30)
        btnLoad.move(30,30)
        btnLoad.setToolTip('Allows choose image from disc.')
        btnLoad.clicked.connect(self.buttonEvent)

        btnStart = QtGui.QPushButton('START', self)
        btnStart.resize(100, 30)
        btnStart.move(30,500)
        btnStart.setToolTip('Starts text recognition.')
        btnStart.clicked.connect(self.buttonEvent)

        font = QtGui.QFont()
        font.setPointSize(10)
        lblImageView = QtGui.QLabel("Image overview", self)
        lblImageView.setFont(font)
        lblImageView.move(30, 80)
        lblImageView = QtGui.QLabel("Recognized text", self)
        lblImageView.setFont(font)
        lblImageView.move(580, 40)

        self.textBox = QtGui.QPlainTextEdit(self)
        self.textBox.move(580, 70)
        self.textBox.resize(500,500)

        self.setGeometry(30, 40, 1130, 610)
        self.backgroundUpdate()
        self.setWindowTitle('Text recognition from raster')
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.show()


    def buttonEvent(self):
        sender = self.sender()
        try:
            if (sender.text() == 'Load image'):
                self.backgroundUpdate()
                self.recognition.setImage()
                image = self.recognition.getImage()
                path = self.recognition.getImagePath()
                self.showImage(image, path)
            else:
                self.recognition.recognize()
                text = self.recognition.getRecognizedText()
                self.textBox.clear()
                self.textBox.insertPlainText(text)
        except IOError:
            QtGui.QMessageBox.question(self, 'Input error', "Please choose image file.", QtGui.QMessageBox.Close)


    def backgroundUpdate(self):
        ''' Hide previous picture choosen by user. '''
        tlo = QtGui.QLabel(self)
        tlo.setPixmap(QtGui.QPixmap('background.png'))
        tlo.move(30,110)
        tlo.resize(506,370)
        tlo.show() 
        
    
    def showImage(self, image, path):
        ''' Show image in GUI. '''
        if (image.size[0]<710 and image.size[1]<356):
            pic = QtGui.QLabel(self)
            pic.setPixmap(QtGui.QPixmap(path))
            pic.move(30+(506-image.size[0])/2, 110+(370-image.size[1])/2)
            pic.resize(image.size[0], image.size[1])
            pic.show()
        else:
            image = self.recognition.resizeImage(0)    
            pic = QtGui.QLabel(self)
            pic.setPixmap(QtGui.QPixmap('picture.png'))
            pic.move(30+(506-image.size[0])/2, 110+(370-image.size[1])/2)
            pic.resize(image.size[0], image.size[1])
            pic.show()


class ImageRecognition(object):
    
    def __init__(self):
        self.imagePath = ""
        self.image = None
        self.text = ""


    def setImage(self):
        self.imagePath = str(QtGui.QFileDialog.getOpenFileName())
        self.image = Image.open(self.imagePath)

    def getImagePath(self):
        return self.imagePath

    def getImage(self):
        return self.image

    def getRecognizedText(self):
        return self.text


    def resizeImage(self, which):
        widthBase = 496
        wpercent = (widthBase/float(self.image.size[0]))
        heightSize = int((float(self.image.size[1])*float(wpercent)))
        if (heightSize < 270):
            im = self.image.resize((widthBase, heightSize), PIL.Image.ANTIALIAS)
            im.save('picture.png')
            return im
        else:
            heightBase = 330
            wpercent = (heightBase/float(self.image.size[1]))
            wSize = int((float(self.image.size[0])*float(wpercent)))
            im = self.image.resize((wSize,heightBase), PIL.Image.ANTIALIAS)
            im.save('picture.png')
            return im

          
    def recognize(self):
        ''' Text recognition on image. '''      
        self.image = cv2.imread(self.imagePath)
        im = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((1, 1), np.uint8)
        im = cv2.dilate(im, kernel, iterations=1)
        im = cv2.erode(im, kernel, iterations=1)
        result = pytesseract.image_to_string(Image.open(self.imagePath))
        self.text = result


def main(): 
    app = QtGui.QApplication(sys.argv)
    myApp = GUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
