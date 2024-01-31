from gui.pages.tab_home import TabHome
from qt_core import *


class Ui_application_pages(object):
    def setupUi(self, application_pages):
        if not application_pages.objectName():
            application_pages.setObjectName(u"application_pages")
        application_pages.resize(1056, 657)
        self.page_home = TabHome()
        self.page_home.setObjectName('page_home')


        application_pages.addWidget(self.page_home)

        QMetaObject.connectSlotsByName(application_pages)
