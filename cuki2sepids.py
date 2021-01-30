from pywinauto.application import Application
import time
import requests
import math
import json


# table address
# app["فروش سالن"]["Edit25"]

# food id in foods window
# app["TKalaToleedFrm"]["Edit5"]

# app = Application(backend="win32").connect(process=5676, title="فروش سالن")
# app = Application(backend="win32").connect(path="D:\SEPIDZ\SEPIDZ\Restaurant.exe", title="فروش سالن")



class Cuki2Cpeds_SaveOrders:
    salonOrder = Application(backend="win32")

    def start(self, path):
        if (self.isCpedsOpen(path)):
            if (self.isSalonOrderOpen()):
                self.salonOrder = self.salonOrder.connect(path=path, title="فروش سالن")
                return True
            else:
                print("لطفا صفحه سفارشات سالن را باز کنید")
                return False
        else:
            print("لطفا نرم افزار سپیدز را باز کنید")
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
                print("غذا با کد " + str(eFood["foodId"]) + "با موفقیت ذخیره شد")
            time.sleep(1)
        except:
            print("خطایی رخ داد")
            print("غذا ثبت نشد")

    def setTable(self, TableNumber):
        try:
            self.salonOrder["فروش سالن"]["Edit25"].send_keystrokes(TableNumber)
            time.sleep(0.5)
            print("میز ثبت شد")
        except:
            print("خطایی رخ داد")
            print("میز ذخیره نشد")

    def saveNoPrint(self):
        try:
            self.salonOrder["فروش سالن"].send_keystrokes("{VK_F2}")
            print("سفارش ثبت  شد")
        except:
            print("خطایی رخ داد")
            print("سفارش ذخیره نشد")


def login():
    url = "https://api.cuki.ir/v201/res/loginRes.fetch.php"

    username = input("Enter Username: ")
    password = input("Enter Password: ")
    loginParams = {
        "username": username,
        "password": password
    }

    r = requests.post(url=url, data=loginParams)
    rData = r.json()
    if rData['statusCode'] == 401:
        print("یوزرنیم یا پسورد اشتباه است. دوباره امتحان کنید")
        login()
    elif rData['statusCode'] == 200:
        print("رستوران:")
        print(rData["data"]["resPersianName"])
        print("خوش آمدید!")
        return rData["data"]
    else:
        print("اتفاقی رخ داد. دوباره امتحان کنید")
        login()


def getOrderList(token):
    url = "https://api.cuki.ir/v201/res/getOrdersList.fetch.php"

    currentTime = math.floor(time.time())
    getOrderListParams = {
        "token": token,
        "startDate": currentTime - 86400,
        "endDate": currentTime
    }

    r = requests.post(url=url, data=getOrderListParams)
    rData = r.json()
    if rData['statusCode'] == 200:
        print(rData["data"])
        return rData["data"]
    else:
        print("اتفاقی رخ داد. دوباره امتحان کنید")
        login()


def getNotSubmittedOrders(ordersList):
    resultArr = []
    for eOrder in ordersList:
        if int(eOrder["counter_app_status"]) == 0:
            orderFoods = {"table": 0, "trackingId": 0, "phone": 0, "foodList": []}
            for eFood in json.loads(eOrder["order_list"]):
                orderFoods["foodList"].append({"foodId": eFood["counterAppFoodId"], "number": eFood['number']})

            orderFoods["table"] = eOrder["order_table"] if int(eOrder["order_table"]) > 0 else eOrder["address"]
            orderFoods["phone"] = eOrder["customer_phone"]
            orderFoods["trackingId"] = eOrder["tracking_id"]
            resultArr.append(orderFoods)
    return resultArr


def importOrderInCpeds(table, foodList, appDirection, action):
    x = Cuki2Cpeds_SaveOrders()
    y = x.start("D:\SEPIDZ\SEPIDZ\Restaurant.exe")
    if y:
        x.setTable("10")
        x.enterFoods([{"foodId": 3, "number": 55}, {"foodId": 1, "number": 66}, {"foodId": 2, "number": 4}, {"foodId": 1448, "number": 123}])
        x.saveNoPrint()


if __name__ == '__main__':
    userInfo = login()
    token = userInfo["token"]
    NotSubmittedOrders = getNotSubmittedOrders(getOrderList(token))
    print(NotSubmittedOrders)
    # import foods:
    cuki2cpeds = Cuki2Cpeds_SaveOrders()
    isAppOpen = cuki2cpeds.start("D:\SEPIDZ\SEPIDZ\Restaurant.exe")
    if isAppOpen:
        for eOrder in NotSubmittedOrders:
            cuki2cpeds.setTable(eOrder['table'])
            cuki2cpeds.enterFoods(eOrder['foodList'])
            cuki2cpeds.saveNoPrint()

