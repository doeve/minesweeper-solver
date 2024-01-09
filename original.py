from random import randint
from turtle import right
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time


dificculty = 2

minevalues = {
    "square blank": -1,
    "square bombflagged": -2,
    "square open0": 0,
    "square open1": 1,
    "square open2": 2,
    "square open3": 3,
    "square open4": 4,
    "square open5": 5,
    "square open6": 6,
    "square open7": 7,
    "square open8": 8,
    "square open9": 9,
}

lines = {
    "hl":  "0 -91px",
    "vl": "-16px -91px",
    "drc": "-32px -91px",
    "dlc": "-48px -91px",
    "urc": "-64px -91px",
    "ulc": "-80px -91px",
    "hrt": "-96px -91px",
    "hlt": "-112px -91px",
    "vut": "-128px -91px",
    "vdt": "0 -108px",
    "eu": "-16px -108px",
    "ed": "-32px -108px",
    "el": "-48px -108px",
    "er": "-64px -108px",
    "cr": "-80px -108px",
    "po": "-96px -108px"
}

# up, down, right, left

line_faces = {
    (0, 0, 1, 1): "hl",
    (1, 1, 0, 0): "vl",
    (0, 1, 1, 0): "drc",
    (0, 1, 0, 1): "dlc",
    (1, 0, 1, 0): "urc",
    (1, 0, 0, 1): "ulc",
    (1, 1, 1, 0): "hrt",
    (1, 1, 0, 1): "hlt",
    (1, 0, 1, 1): "vut",
    (0, 1, 1, 1): "vdt",
    (1, 0, 0, 0): "eu",
    (0, 1, 0, 0): "ed",
    (0, 0, 0, 1): "el",
    (0, 0, 1, 0): "er",
    (1, 1, 1, 1): "cr",
    (0, 0, 0, 0): "po"
}


ws_sizes = [[9, 9, "#beginner"], [16, 16, "#intermediate"], [16, 30, ""]]
w = ws_sizes[dificculty - 1][0]
h = ws_sizes[dificculty - 1][1]

print(str(w) + " " + str(h))
called = 0


to_expl = []
explored = [[0 for _ in range(w + 2)] for _ in range(h + 2)]


def change_face(sel_x, sel_y, s):
    driver.execute_script("document.getElementById('" + str(sel_y) +
                          "_" + str(sel_x) + "').style.backgroundPosition = '" + lines[line_faces[s]] + "'")


def minefield(x, y):
    global called
    called += 1
    if (x == 0) or (x == w + 1) or (y == 0) or (y == h + 1):
        return -1
    else:
        element = driver.find_element(By.ID ,str(y) + "_" + str(x))
        return minevalues[element.get_attribute("class")]


def rightclick(x, y):
    action = ActionChains(driver)
    found_flag = driver.find_element(By.ID ,
        str(y) + "_" + str(x))
    action.context_click(found_flag).perform()


def around(sel_x, sel_y, s):
    sum = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if sel_x + i != 0 and sel_x + i != w + 1 and sel_y + j != 0 and sel_y + j != h + 1:
                if minefield(sel_x + i, sel_y + j) == s:
                    sum += 1
    return sum


def auxentios(sel_x, sel_y):
    print("auxentios: " + str(sel_y) + "_" + str(sel_x) + " / around: -1: " +
          str(around(sel_x, sel_y, -1)) + ", -2: " + str(around(sel_x, sel_y, -2)))
    if around(sel_x, sel_y, -1) + around(sel_x, sel_y, -2) == minefield(sel_x, sel_y) and around(sel_x, sel_y, -1) != 0:
        print("entered flags:")
        for i in range(-1, 2):
            for j in range(-1, 2):
                if sel_x + i != 0 and sel_x + i != w + 1 and sel_y + j != 0 and sel_y + j != h + 1:
                    if minefield(sel_x + i, sel_y + j) == -1:
                        rightclick(sel_x + i, sel_y + j)
                        print("    clicked: " + str(sel_y + j) +
                              "_" + str(sel_x + i))
                        for m in range(-1, 2):
                            for n in range(-1, 2):
                                if not (m == 0 and n == 0):
                                    if sel_x + i + m != 0 and sel_x + i + m != w + 1 and sel_y + j + n != 0 and sel_y + j + n != h + 1:
                                        if minefield(sel_x + i + m, sel_y + j + n) > 0:
                                            auxentios(sel_x + i + m,
                                                      sel_y + j + n)
                        #                 bion()

    elif around(sel_x, sel_y, -2) == minefield(sel_x, sel_y):
        print("entered purging")
        for i in range(-1, 2):
            for j in range(-1, 2):
                if sel_x + i != 0 and sel_x + i != w + 1 and sel_y + j != 0 and sel_y + j != h + 1:
                    if minefield(sel_x + i, sel_y + j) == -1:
                        driver.find_element(By.ID ,
                            str(sel_y + j) + "_" + str(sel_x + i)).click()
                        for m in range(-1, 2):
                            for n in range(-1, 2):
                                if not (m == 0 and n == 0):
                                    if sel_x + i + m != 0 and sel_x + i + m != w + 1 and sel_y + j + n != 0 and sel_y + j + n != h + 1:
                                        if minefield(sel_x + i + m, sel_y + j + n) > 0:
                                            auxentios(sel_x + i + m,
                                                      sel_y + j + n)
                        if minefield(sel_x + i, sel_y + j) == 0:
                            aristarchus(sel_x + i, sel_y + j,
                                        sel_x + i, sel_y + j)
                        elif minefield(sel_x + i, sel_y + j) > 0:
                            auxentios(sel_x + i, sel_y + j)


def find_face(sel_x, sel_y, last_x, last_y):
    h = sel_x - last_x
    v = sel_y - last_y
    aux_tuple = list(faces[last_y][last_x])
    if h == 1:
        aux_tuple[2] = 1
    if h == -1:
        aux_tuple[3] = 1
    if v == -1:
        aux_tuple[0] = 1
    if v == 1:
        aux_tuple[1] = 1
    faces[last_y][last_x] = tuple(aux_tuple)
    change_face(last_x, last_y, faces[last_y][last_x])
    aux_tuple = list(faces[sel_y][sel_x])
    if h == -1:
        aux_tuple[2] = 1
    if h == 1:
        aux_tuple[3] = 1
    if v == 1:
        aux_tuple[0] = 1
    if v == -1:
        aux_tuple[1] = 1
    faces[sel_y][sel_x] = tuple(aux_tuple)
    change_face(sel_x, sel_y, faces[sel_y][sel_x])
    print("sel x: " + str(sel_x) + " sel y:" + str(sel_y) +
          " last x: " + str(last_x) + " last y: " + str(last_y))


def aristarchus(sel_x, sel_y, last_x, last_y):
    if minefield(sel_x, sel_y) >= 0:
        if sel_x - last_x == 0 and sel_y - last_y == 0:
            change_face(sel_x, sel_y, (0, 0, 0, 0))
        else:
            find_face(sel_x, sel_y, last_x, last_y)
    explored[sel_y][sel_x] = -1
    print(str(sel_y) + " " + str(sel_x) + " " + str(minefield(sel_x, sel_y)))
    print("exploring " + str(sel_y) + "_" + str(sel_x) +
          " faces are " + str(faces[sel_y][sel_x]) + " old faces are " + str(faces[last_y][last_x]))

    if minefield(sel_x, sel_y) > 0:
        auxentios(sel_x, sel_y)

    if explored[sel_y][sel_x + 1] != -1 and minefield(sel_x + 1, sel_y) >= 0:
        aristarchus(sel_x + 1, sel_y, sel_x, sel_y)
    if explored[sel_y + 1][sel_x] != -1 and minefield(sel_x, sel_y + 1) >= 0:
        aristarchus(sel_x, sel_y + 1, sel_x, sel_y)
    if explored[sel_y][sel_x - 1] != -1 and minefield(sel_x - 1, sel_y) >= 0:
        aristarchus(sel_x - 1, sel_y, sel_x, sel_y)
    if explored[sel_y - 1][sel_x] != -1 and minefield(sel_x, sel_y - 1) >= 0:
        aristarchus(sel_x, sel_y - 1, sel_x, sel_y)


link = ws_sizes[dificculty - 1][2]
faces = [[(0, 0, 0, 0) for _ in range(1, w + 2)] for _ in range(1, h + 2)]

driver = webdriver.Chrome()
driver.get("https://minesweeperonline.com/" + link)
driver.execute_script(
    "var style = document.createElement('style'); style.type = 'text/css'; style.innerHTML = '.z100 #game div {background-image: url(https://i.ibb.co/Wgt8D9d/sprite100.gif);}'; document.getElementsByTagName('head')[0].appendChild(style);")

driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div[2]/div[2]/button[1]').click()

sel_x = randint(1, h)
sel_y = randint(1, w)
driver.find_element(By.ID ,str(sel_y) + "_" +
                          str(sel_x)).click()
# change_face(sel_x, sel_y, "po")

aristarchus(sel_x, sel_y, sel_x, sel_y)

print("im done for whatever reason, i was called " + str(called) + " times.")

time.sleep(5)
