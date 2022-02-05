import sys
import os
import requests

from PIL import Image, ImageQt
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon

SCREEN_SIZE = [400, 400]


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_win.ui", self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Карта")
        self.setWindowIcon(QIcon("yandex.png"))
        self.download_pic("МГУ")
        self.map_file = "map.bmp"

    def download_pic(self, adress):
        position = self.get_position(adress)
        print(position)
        map_request = "https://static-maps.yandex.ru/1.x/"
        params = {
            "l": "sat",
            "ll": position,
            "z": 4
        }
        response = requests.get(map_request, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.

        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def get_position(self, adress):
        geocoder_request = "http://geocode-maps.yandex.ru/1.x/"

        params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": adress,
            "format": "json"
        }
        response = requests.get(geocoder_request, params=params)
        if response:
            json_response = response.json()
            position = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
                "Point"]["pos"]
            return position
        return [None, None]

    def change_color(self):  # необходимо всякий раз работать с self.im, и заново инициализировать
        # (и загружать в виджет) self.picture.
        if self.sender().text() == "R":
            self.return_picture(self.im_pixels, self.im)
            pixels = self.im.load()
            x, y = self.im.size
            for i in range(x):
                for j in range(y):
                    r, g, b = pixels[i, j]
                    r = 255
                    pixels[i, j] = r, g, b
            self.repainting()
        elif self.sender().text() == "G":
            self.return_picture(self.im_pixels, self.im)
            pixels = self.im.load()
            x, y = self.im.size
            for i in range(x):
                for j in range(y):
                    r, g, b = pixels[i, j]
                    g = 255
                    pixels[i, j] = r, g, b
            self.repainting()
        elif self.sender().text() == "B":
            self.return_picture(self.im_pixels, self.im)
            pixels = self.im.load()
            x, y = self.im.size
            for i in range(x):
                for j in range(y):
                    r, g, b = pixels[i, j]
                    b = 255
                    pixels[i, j] = r, g, b
            self.repainting()
        else:
            self.return_picture(self.im_pixels, self.im)
            self.repainting()

    def turn(self):
        if self.sender().text() == "Повернуть по часовой стрелке":
            self.im = self.im.transpose(Image.ROTATE_270)
            self.im1 = self.im1.transpose(Image.ROTATE_270)
            self.im_pixels = self.im1.load()
            self.repainting()
        else:
            self.im = self.im.transpose(Image.ROTATE_90)
            self.im1 = self.im1.transpose(Image.ROTATE_90)
            self.im_pixels = self.im1.load()
            self.repainting()

    def return_picture(self, pixels_first, picture):
        pixels = picture.load()
        x, y = picture.size
        for i in range(x):
            for j in range(y):
                pixels[i, j] = pixels_first[i, j]

    def repainting(self):
        qim = ImageQt.ImageQt(self.im)
        self.pixmap = QPixmap.fromImage(qim)
        self.picture.setPixmap(self.pixmap.copy())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

# import os
# import sys
#
# import pygame
# import requests
#
# map_request = "https://static-maps.yandex.ru/1.x/?l=sat&ll=136.387307%2C-28.689820&mode=search&" \
#               "ol=geo&ouri=ymapsbm1%3A%2F%2Fgeo%3Fll%3D133.795%252C-25.695%26spn%3D86.4" \
#               "64%252C45.780%26text%3DAustralia&source=wizgeo&utm_medium=maps-desktop&utm_source=serp&z=4"
# response = requests.get(map_request)
#
# if not response:
#     print("Ошибка выполнения запроса:")
#     print(map_request)
#     print("Http статус:", response.status_code, "(", response.reason, ")")
#     sys.exit(1)
#
# # Запишем полученное изображение в файл.
# map_file = "map.bmp"
# with open(map_file, "wb") as file:
#     file.write(response.content)
#
# # Инициализируем pygame
# pygame.init()
# screen = pygame.display.set_mode((600, 450))
# # Рисуем картинку, загружаемую из только что созданного файла.
# screen.blit(pygame.image.load(map_file), (0, 0))
# # Переключаем экран и ждем закрытия окна.
# pygame.display.flip()
# while pygame.event.wait().type != pygame.QUIT:
#     pass
# pygame.quit()
#
# # Удаляем за собой файл с изображением.
# os.remove(map_file)
