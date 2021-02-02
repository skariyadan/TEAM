import gui
import cli
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

def main():
    #cli.main()

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('mouse.PNG'))
    manager = gui.Manager()
    sys.exit(app.exec_())
#    app = gui.Team_GUI()
 #   app.run()



if __name__ == "__main__":
    main()


