import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QLineEdit, QListWidget,\
    QListWidgetItem, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(800, 300, 500, 500)
        self.setWindowTitle('Каталог библиотеки')

        self.cb = QComboBox(self)
        self.cb.addItems(["Автор", "Название"])
        self.cb.move(30, 30)
        self.cb.resize(120, 30)

        self.le = QLineEdit(self)
        self.le.move(30, 90)

        self.btn = QPushButton("Искать", self)
        self.btn.move(220, 20)
        self.btn.resize(150, 80)
        self.btn.clicked.connect(self.click)

        self.lw = QListWidget(self)
        self.lw.move(20, 140)
        self.lw.resize(460, 340)
        self.lw.itemClicked.connect(self.click1)

    def click(self):
        if self.le.text() != '':
            if self.cb.currentText() == 'Название':
                con = sqlite3.connect('books.sqlite')
                cur = con.cursor()
                nam = self.le.text()
                zap = f"SELECT name FROM books WHERE name LIKE '%{nam}%' "
                res = cur.execute(zap).fetchall()
                self.lw.clear()
                for i in res:
                    item = QListWidgetItem(i[0])
                    item.setTextAlignment(Qt.AlignHCenter)
                    self.lw.addItem(item)
                con.commit()
                con.close()
            elif self.cb.currentText() == 'Автор':
                con = sqlite3.connect('books.sqlite')
                cur = con.cursor()
                nam = self.le.text()
                zap = f"SELECT name FROM books WHERE author_id = (SELECT id from authors WHERE author LIKE '%{nam}%') "
                res = cur.execute(zap).fetchall()
                self.lw.clear()
                for i in res:
                    item = QListWidgetItem(i[0])
                    item.setTextAlignment(Qt.AlignHCenter)
                    self.lw.addItem(item)
                con.commit()
                con.close()

    def click1(self):
        global name
        name = self.lw.currentItem().text()
        self.w = Example1()
        self.w.show()


class Example1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(860, 310, 400, 600)
        self.setWindowTitle('Информация о книге')

        con = sqlite3.connect('books.sqlite')
        cur = con.cursor()
        zap = f"SELECT picture FROM books WHERE name = '{name}'"
        res = cur.execute(zap).fetchall()
        con.commit()
        con.close()
        self.pixmap = QPixmap(res[0][0])
        self.pixmap = self.pixmap.scaledToWidth(200)
        self.image = QLabel(self)
        self.image.move(100, 30)
        self.image.resize(200, 300)
        self.image.setPixmap(self.pixmap)

        self.lbl1 = QLabel('Название', self)
        self.lbl1.move(125, 340)
        self.lbl1.setFont(QFont('Arial', 20))

        self.lbl1_n = QLabel(name, self)
        self.lbl1_n.move(0, 380)
        self.lbl1_n.setAlignment(Qt.AlignHCenter)
        self.lbl1_n.setFont(QFont('Arial', 10))
        self.lbl1_n.resize(400, 30)

        self.lbl2 = QLabel('Автор', self)
        self.lbl2.move(155, 400)
        self.lbl2.setFont(QFont('Arial', 20))

        con = sqlite3.connect('books.sqlite')
        cur = con.cursor()
        zap = f"SELECT author FROM authors WHERE id = (SELECT author_id FROM books WHERE name = '{name}')"
        res = cur.execute(zap).fetchall()
        con.commit()
        con.close()
        self.lbl2_n = QLabel(res[0][0], self)
        self.lbl2_n.move(0, 440)
        self.lbl2_n.setAlignment(Qt.AlignHCenter)
        self.lbl2_n.setFont(QFont('Arial', 10))
        self.lbl2_n.resize(400, 30)

        self.lbl3 = QLabel('Год выпуска', self)
        self.lbl3.move(105, 460)
        self.lbl3.setFont(QFont('Arial', 20))

        con = sqlite3.connect('books.sqlite')
        cur = con.cursor()
        zap = f"SELECT year FROM years WHERE id = (SELECT year_id FROM books WHERE name = '{name}')"
        res = cur.execute(zap).fetchall()
        con.commit()
        con.close()
        self.lbl3_n = QLabel(str(res[0][0]), self)
        self.lbl3_n.move(0, 500)
        self.lbl3_n.setAlignment(Qt.AlignHCenter)
        self.lbl3_n.setFont(QFont('Arial', 10))
        self.lbl3_n.resize(400, 30)

        self.lbl4 = QLabel('Жанр', self)
        self.lbl4.move(155, 520)
        self.lbl4.setFont(QFont('Arial', 20))

        con = sqlite3.connect('books.sqlite')
        cur = con.cursor()
        zap = f"SELECT genre FROM genres WHERE id = (SELECT genre_id FROM books WHERE name = '{name}')"
        res = cur.execute(zap).fetchall()
        con.commit()
        con.close()
        self.lbl4_n = QLabel(res[0][0], self)
        self.lbl4_n.move(0, 560)
        self.lbl4_n.setAlignment(Qt.AlignHCenter)
        self.lbl4_n.setFont(QFont('Arial', 10))
        self.lbl4_n.resize(400, 30)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())