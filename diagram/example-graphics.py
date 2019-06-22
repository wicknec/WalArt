#-*- coding:utf-8 -*-  
  
from PyQt4.QtCore import *  
from PyQt4.QtGui import *  
import math  
  
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf-8"))  
  
class FlashItem(QGraphicsItem):  
    def __init__(self,QObject):  
        super(FlashItem,self).__init__()  
        self.timer = QTimer()  
        self.flash = True  
        self.setFlag(self.ItemIsMovable)  
        aa=QObject()  
        aa.startTimer(50)  
      
    def boundingRect(self):  
        adjust = 2  
        return QRectF(-10 - adjust,-10 - adjust,43 + adjust,43 + adjust)  
      
    def paint(self,painter,option,widget):  
        painter.setPen(Qt.NoPen)  
        painter.setBrush(Qt.darkGray)  
        painter.drawEllipse(-7,-7,40,40)  
          
        painter.setPen(QPen(Qt.black,0))  
        painter.setBrush(self.flash if Qt.red else Qt.yellow)  
        painter.drawEllipse(-10,-10,40,40)  
      
    def timerEvent(self,QTimerEvent):  
        self.flash = not flash  
        self.update()  
  
class StarItem(QGraphicsItem):  
    def __init__(self):  
        super(StarItem,self).__init__()  
        self.fix = QPixmap()  
        self.fix.load("image/star.png")  
      
    def boundingRect(self):  
        return QRectF(-self.fix.width()/2,-self.fix.height()/2,self.fix.width(),self.fix.height())  
      
    def paint(self,painter,option,widget):  
        painter.drawPixmap(self.boundingRect().topLeft(),self.fix)  
          
          
class MainWindow(QMainWindow):  
    def __init__(self,QWidget):  
        super(MainWindow,self).__init__()  
        self.createActions()  
        self.createMenus()  
                  
        self.scene = QGraphicsScene(self)  
        self.scene.setSceneRect(-200,-200,600,600)  
        self.initScene()  
          
        self.view = QGraphicsView()  
        self.view.setScene(self.scene)  
        self.view.setMinimumSize(600,600)  
        self.view.show()  
          
        self.setCentralWidget(self.view)  
        self.resize(800,600)  
        self.setWindowTitle(self.tr("各种Graphics Items"))  
      
    def createActions(self):  
        self.newAct = QAction(self.tr("New"),self)  
        self.connect(self.newAct,SIGNAL("triggered()"),self.slotNew)  
          
        self.clearAct = QAction(self.tr("Clear"),self)  
        self.connect(self.clearAct,SIGNAL("triggered()"),self.slotCrear)  
          
        self.exitAct = QAction(self.tr("Exit"),self)  
        self.addEllipseItemAct = QAction(self.tr("Add Ellipse"),self)  
        self.addPolygonItemAct = QAction(self.tr("Add Polygon"),self)  
        self.addTextItemAct = QAction(self.tr("Add Text"),self)  
        self.addFlashItemAct = QAction(self.tr("Add Flash"),self)  
        self.addRectItemAct = QAction(self.tr("Add Rectangle"),self)  
        self.addAnimItemAct = QAction(self.tr("Add Animation"),self)  
        self.addAlphaItemAct = QAction(self.tr("Add Alpha-png"),self)  
      
    def createMenus(self):  
        fileMenu = self.menuBar().addMenu(self.tr("File"))  
        fileMenu.addAction(self.newAct)  
        fileMenu.addAction(self.clearAct)  
        fileMenu.addAction(self.exitAct)  
        fileMenu.addAction(self.addEllipseItemAct)  
        fileMenu.addAction(self.addPolygonItemAct)  
        fileMenu.addAction(self.addTextItemAct)  
        fileMenu.addAction(self.addFlashItemAct)  
        fileMenu.addAction(self.addRectItemAct)  
        fileMenu.addAction(self.addAnimItemAct)  
        fileMenu.addAction(self.addAlphaItemAct)  
      
    def initScene(self):  
        for i in range(3):  
            self.slotAddFlashItem()  
        for i in range(3):  
            self.slotAddEllipseItem()  
        for i in range(3):  
            self.slotAddRectItem()  
        for i in range(3):  
            self.slotAddAlphaItem()  
        for i in range(3):  
            self.slotAddPolygonItem()  
        for i in range(3):  
            self.slotAddTextItem()  
        for i in range(3):  
            self.slotAddAnimationItem()  
          
      
    def slotNew(self):  
        self.slotCrear()  
        self.initScene()  
        newWin = MainWindow(self)  
        newWin.show()  
      
    def slotCrear(self):  
        listItem = self.scene.items()  
        while(len(listItem) != 0):  
            self.scene.removeItem(listItem[0])  
            listItem.remove(listItem[0])  
      
    def slotAddEllipseItem(self):  
        item = QGraphicsEllipseItem(QRectF(0,0,80,60))  
        item.setPen(QPen(Qt.NoPen))  
        item.setBrush(QColor(qrand()%256,qrand()%256,qrand()%256))  
        scale = ((qrand()%10)+1)/5.0  
        item.scale(scale,scale)  
        item.setFlag(QGraphicsItem.ItemIsMovable)  
        self.scene.addItem(item)  
        item.setPos((qrand()%int(self.scene.sceneRect().width())) - 200,(qrand()%int(self.scene.sceneRect().height())) - 200)  
      
    def slotAddPolygonItem(self):  
        v = [QPointF(30,-15),QPointF(0,-30),QPointF(30,-15),QPointF(30,-15),QPointF(0,30),QPointF(30,15)]  
        item = QGraphicsPolygonItem(QPolygonF(v))  
        item.setBrush(QColor(qrand()%256,qrand()%256,qrand()%256))  
        item.setFlag(QGraphicsItem.ItemIsMovable)  
        self.scene.addItem(item)  
        item.setPos((qrand()%int(self.scene.sceneRect().width())) - 200,(qrand()%int(self.scene.sceneRect().height())) - 200)  
          
    def slotAddRectItem(self):  
        item = QGraphicsRectItem(QRectF(0,0,60,60))  
        pen = QPen()  
        pen.setWidth(3)  
        pen.setColor(QColor(qrand()%256,qrand()%256,qrand()%256))  
        item.setPen(pen)  
        item.setBrush(QColor(qrand()%256,qrand()%256,qrand()%256))  
        item.setFlag(QGraphicsItem.ItemIsMovable)  
        self.scene.addItem(item)  
        item.setPos((qrand()%int(self.scene.sceneRect().width())) - 200,(qrand()%int(self.scene.sceneRect().height())) - 200)  
      
    def slotAddTextItem(self):  
        font = QFont("Times",16)  
        item = QGraphicsTextItem("Hello Qt")  
        item.setFont(font)  
        item.setFlag(QGraphicsItem.ItemIsMovable)  
        item.setDefaultTextColor(QColor(qrand()%256,qrand()%256,qrand()%256))  
        self.scene.addItem(item)  
        item.setPos((qrand()%int(self.scene.sceneRect().width())) - 200,(qrand()%int(self.scene.sceneRect().height())) - 200)  
      
    def slotAddFlashItem(self):  
        item = FlashItem(QObject)  
        scale = ((qrand()%10) + 1)/5.0  
        item.scale(scale,scale)  
        self.scene.addItem(item)  
        item.setPos((qrand()%int(self.scene.sceneRect().width())) - 200,(qrand()%int(self.scene.sceneRect().height())) - 200)  
      
    def slotAddAlphaItem(self):  
        item = self.scene.addPixmap(QPixmap("image/butterfly.png"))  
        item.setFlag(QGraphicsItem.ItemIsMovable)  
        item.setPos((qrand()%int(self.scene.sceneRect().width())) - 200,(qrand()%int(self.scene.sceneRect().height())) - 200)  
      
    def slotAddAnimationItem(self):  
        item = StarItem()  
        anim = QGraphicsItemAnimation()  
        anim.setItem(item)  
        timeLine = QTimeLine(4000)  
        timeLine.setCurveShape(QTimeLine.SineCurve)  
        timeLine.setLoopCount(0)  
        anim.setTimeLine(timeLine)  
        y = (qrand()%800) - 600  
        for i in range(800):  
            anim.setPosAt(i/800.0,QPointF(i - 600,y))  
        timeLine.start()  
        self.scene.addItem(item)  
  
if __name__ == '__main__':  
    import sys  
    app = QApplication(sys.argv)  
    mainwindow = MainWindow(QWidget)  
    mainwindow.show()  
    sys.exit(app.exec_())  
