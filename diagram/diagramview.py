'''
WalArt.diagram
=============================
Walnut Artifacts

Created by wicknec 2015
wicknec@gmail.com

Partly simulates Qt DiagramScene
(http://doc.qt.io/qt-5/qtwidgets-graphicsview-diagramscene-example.html#arrow-class-definition)
to show concept relations

'''
#-*- coding:utf-8 -*-  
'''
Revisions:
==============================
160218 implemented Arrow
160219 implemented Note, debugged
'''

from PyQt4.QtCore import *  
from PyQt4.QtGui import *  
import math  
  
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf-8"))  

class StarItem(QGraphicsItem):  
    def __init__(self):  
        super(StarItem,self).__init__()  
        self.fix = QPixmap()  
        self.fix.load("image/star.png")  
      
    def boundingRect(self):  
        return QRectF(-self.fix.width()/2,-self.fix.height()/2,self.fix.width(),self.fix.height())  
      
    def paint(self,painter,option,widget):  
        painter.drawPixmap(self.boundingRect().topLeft(),self.fix)  

class Arrow(QGraphicsLineItem):
    def __init__(self,src,dst,parent=None):
        super(Arrow,self).__init__()
        self.src=src
        self.dst=dst
        self.parent=parent
        self.setFlag(QGraphicsItem.ItemIsSelectable,True)
        self.color=Qt.black
        self.setPen(QPen(self.color,3,Qt.SolidLine,Qt.RoundCap,Qt.RoundJoin))
        self.arrowHead=QPolygonF()
        self.arrowSize=10
        
    def boundingRect(self):
        extra=(self.pen().width()+20)/2
        return QRectF(self.line().p1(),QSizeF(self.line().p2().x()-self.line().p1().x(),\
                                              self.line().p2().y()-self.line().p1().y()))\
                                              .normalized()\
                                              .adjusted(-extra,-extra,extra,extra)


    def shape(self):
        path=super(Arrow,self).shape()
        path.addPolygon(self.arrowHead)
        return path
    
    def setColor(self,color):
        self.color=color

    def updatePosition(self):
        line=QLineF(self.mapFromItem(self.src,0,0),self.mapFromItem(self.dst,0,0))
        self.setLine(line)

    def paint(self,painter,option,widget):
        if self.src.collidesWithItem(self.dst):
            return
        myPen=self.pen()
        arrowSize=20
        painter.setPen(myPen)
        painter.setBrush(self.color)

        centerLine=QLineF(self.src.pos(),self.dst.pos())
        endPolygon=self.dst.polygon()
        p1=endPolygon.first()+self.dst.pos()
        intersectPoint=QPointF()

        for i in range(endPolygon.count()):
            p2=endPolygon.at(i+1)+self.dst.pos()
            polyLine=QLineF(p1,p2)
            intersectType=polyLine.intersect(centerLine,intersectPoint)
            if intersectType==QLineF.BoundedIntersection:
                break
            p1=p2
        self.setLine(QLineF(intersectPoint,self.src.pos()))

        angle=math.acos(self.line().dx()/self.line().length())
        if self.line().dy()>=0:
            angle=math.pi*2-angle
        arrowP1=self.line().p1()+QPointF(math.sin(angle+math.pi/3)*self.arrowSize,
                                         math.cos(angle+math.pi/3)*self.arrowSize)
        arrowP2=self.line().p1()+QPointF(math.sin(angle+math.pi*2/3)*self.arrowSize,
                                         math.cos(angle+math.pi*2/3)*self.arrowSize)
        self.arrowHead.clear()
        self.arrowHead.append(self.line().p1())
        self.arrowHead.append(arrowP1)
        self.arrowHead.append(arrowP2)

        painter.drawLine(self.line())
        painter.drawPolygon(self.arrowHead)
        self.src.setZValue(self.zValue()+1)
        
        if self.isSelected():
            painter.setPen(QPen(self.color,1,Qt.DashLine))
            myLine=self.line()
            myLine.translate(0,4)
            painter.drawLine(myLine)
            myLine.translate(0,-8)
            painter.drawLine(myLine)

def RegularPolygon(n,rot,radius):
    '''rot is a float usually between [0,1) signfies the rotation to the fraction of each polygon sides
'''
    p=QPolygonF()
    rot=math.pi*2/n*rot
    for a in range(n):
        p.append(QPointF(math.cos(math.pi*2/n*a+rot)*radius,
                         math.sin(math.pi*2/n*a+rot)*radius))
    return p
class Note(QGraphicsPolygonItem):
    '''
'''
    def __init__(self,text='Hello Qt\n哈哈'):
        super(Note,self).__init__()
        self.setPolygon(RegularPolygon(8,0.5,50))
        item = QGraphicsTextItem(text)
        item.setParentItem(self)
        self.textItem=item
        self.setScale(1)
        self.setFlag(QGraphicsItem.ItemIsSelectable,True)
        
    def setScale(self,factor):
        self.setPolygon(RegularPolygon(8,0.5,50*factor))
        font = QFont("Times",10*factor)        
        self.textItem.setFont(font)

        self.textItem.setPos(-40*factor,-20*factor)

        textop=QTextOption(Qt.AlignCenter)
        
        self.textItem.document().setDefaultTextOption(textop)
        self.textItem.document().setTextWidth(80*factor)
        #item.document().setPageSize(QSizeF(80,80))
        #print(item.document().pageSize())

        
        
          
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
            self.slotAddEllipseItem()
        notes=[]
        for i in range(4):
            notes.append(self.slotAddNote())
        for i in range(3):
            a=Arrow(notes[i],notes[i+1])
            a.setFlag(QGraphicsItem.ItemIsMovable)  
            self.scene.addItem(a)
          
      
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
      
    def slotAddTextItem(self):  
        font = QFont("Times",16)  
        item = QGraphicsTextItem("Hello Qt")  
        item.setFont(font)  
        item.setFlag(QGraphicsItem.ItemIsMovable)  
        item.setDefaultTextColor(QColor(qrand()%256,qrand()%256,qrand()%256))  
        self.scene.addItem(item)  
        item.setPos((qrand()%int(self.scene.sceneRect().width())) - 200,(qrand()%int(self.scene.sceneRect().height())) - 200)  

    def slotAddNote(self):  
        font = QFont("Times",16)  
        item = Note()  
        item.setFlag(QGraphicsItem.ItemIsMovable)  
        item.setPen(QPen(Qt.NoPen))  
        item.setBrush(QColor(qrand()%256,qrand()%256,qrand()%256))
        scale = ((qrand()%10)+1)/5.0  
        item.setScale(scale)  
        self.scene.addItem(item)  
        item.setPos((qrand()%int(self.scene.sceneRect().width())) - 200,(qrand()%int(self.scene.sceneRect().height())) - 200)
        return item
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
