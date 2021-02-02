from pywinauto.application import Application
import time


class Cuki2Cpeds_SaveOrders:
    salonOrder = Application(backend="win32")
    statusLabel = ""

    def __init__(self, statusLabel):
        self.statusLabel = statusLabel

    def start(self, path):
        if self.isCpedsOpen(path):
            if self.isSalonOrderOpen():
                self.salonOrder = self.salonOrder.connect(path=path, title="فروش سالن")
                return True
            else:
                print("لطفا صفحه سفارشات سالن را باز کنید")
                self.statusLabel.config(text="لطفا صفحه سفارشات سالن را باز کنید")
                return False
        else:
            print("لطفا نرم افزار سپیدز را باز کنید")
            self.statusLabel.config(text="لطفا نرم افزار سپیدز را باز کنید")
            return False

    def isCpedsOpen(self, path):
        try:
            self.salonOrder.connect(path=path, title="فروش سالن")
            return True
        except:
            return False

    def isSalonOrderOpen(self):
        try:
            self.salonOrder["فروش سالن"].child_window(title="Panel2", class_name="TPanel").child_window(
                class_name="TStringGrid").send_keystrokes("{SPACE}")
            return True
        except:
            return False

    def salonIsTopWindow(self):
        if self.salonOrder.top_window().element_info.name == "فروش سالن":
            return True
        else:
            self.statusLabel.config(text="صفحات اضافه را ببندید. تنها ثبت سفارش باز باشد")
            return False

    def enterFoods(self, foodsArr):

        try:
            for eFood in foodsArr:
                self.salonOrder["فروش سالن"].child_window(title="Panel2", class_name="TPanel").child_window(
                    class_name="TStringGrid").send_keystrokes(str(eFood["foodId"]))
                self.salonOrder["فروش سالن"].child_window(title="Panel2", class_name="TPanel").child_window(
                    class_name="TStringGrid").send_keystrokes("{ENTER}")
                self.salonOrder["فروش سالن"].child_window(title="Panel2", class_name="TPanel").child_window(
                    class_name="TStringGrid").send_keystrokes(str(eFood["number"]))
                self.salonOrder["فروش سالن"].child_window(title="Panel2", class_name="TPanel").child_window(
                    class_name="TStringGrid").send_keystrokes("{ENTER}")
            time.sleep(0.2)
        except:
            self.statusLabel.config(text="!خطایی رخ داد. غذا ثبت نشد")
            print("خطایی رخ داد")
            print("غذا ثبت نشد")

    def setTable(self, TableNumber):
        try:
            for _ in range(6):
                self.salonOrder["فروش سالن"]["Edit25"].send_keystrokes("{BACKSPACE}")
            self.salonOrder["فروش سالن"]["Edit25"].send_keystrokes(TableNumber)
            time.sleep(0.2)
            self.statusLabel.config(text="میز ثبت شد")
            print("میز ثبت شد")
        except:
            self.statusLabel.config(text="!خطایی رخ داد. میز ذخیره نشد")
            print("خطایی رخ داد")
            print("میز ذخیره نشد")

    def saveNoPrint(self):
        try:
            self.salonOrder["فروش سالن"].send_keystrokes("{VK_F2}")
            print("سفارش ثبت  شد")
            self.statusLabel.config(text="سفارش ثبت  شد")
            return True
        except:
            self.statusLabel.config(text="!خطایی رخ داد. سفارش ذخیره نشد")
            print("خطایی رخ داد")
            print("سفارش ذخیره نشد")
            return False
