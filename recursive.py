from random import randint
from turtle import right
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


dificculty = 3
skin = 'roses'

# skin - https://i.ibb.co/BCVtQ3x/sprite100-skinned.gif
# original - https://i.ibb.co/pRnqDqt/sprite100.gif
# roses - https://i.ibb.co/h14qBg3/sprite100-roses.gif

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
    "vdt": "0 -107px",
    "eu": "-16px -107px",
    "ed": "-32px -107px",
    "el": "-48px -107px",
    "er": "-64px -107px",
    "cr": "-80px -107px",
    "po": "-96px -107px"
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


ws_sizes = [[9, 9, "#beginner", 10], [
    16, 16, "#intermediate", 40], [16, 30, "", 99]]
h = ws_sizes[dificculty - 1][0]
w = ws_sizes[dificculty - 1][1]
mine_matrix = [[-1 for _ in range(w + 2)] for _ in range(h + 2)]
mines = 0

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
        element = driver.find_element(By.ID, str(y) + "_" + str(x))
        return minevalues[element.get_attribute("class")]


def rightclick(x, y):
    global mines
    mines += 1
    action = ActionChains(driver)
    found_flag = driver.find_element(By.ID, 
        str(y) + "_" + str(x))
    action.context_click(found_flag).perform()


def around(sel_x, sel_y, s):
    sum = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if sel_x + i != 0 and sel_x + i != w + 1 and sel_y + j != 0 and sel_y + j != h + 1:
                if mine_matrix[sel_y + j][sel_x + i] == s:
                    sum += 1
    return sum


def auxentios(sel_x, sel_y):
    if around(sel_x, sel_y, -1) + around(sel_x, sel_y, -2) == mine_matrix[sel_y][sel_x] and around(sel_x, sel_y, -1) != 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if sel_x + i != 0 and sel_x + i != w + 1 and sel_y + j != 0 and sel_y + j != h + 1:
                    if mine_matrix[sel_y + j][sel_x + i] == -1:
                        rightclick(sel_x + i, sel_y + j)
                        mine_matrix[sel_y + j][sel_x + i] = -2
                        for m in range(-1, 2):
                            for n in range(-1, 2):
                                if not (m == 0 and n == 0):
                                    if sel_x + i + m != 0 and sel_x + i + m != w + 1 and sel_y + j + n != 0 and sel_y + j + n != h + 1:
                                        if mine_matrix[sel_y + j + n][sel_x + i + m] > 0:
                                            auxentios(sel_x + i + m,
                                                      sel_y + j + n)

    elif around(sel_x, sel_y, -2) == mine_matrix[sel_y][sel_x]:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if sel_x + i != 0 and sel_x + i != w + 1 and sel_y + j != 0 and sel_y + j != h + 1:
                    if mine_matrix[sel_y + j][sel_x + i] == -1:
                        driver.find_element(By.ID, 
                            str(sel_y + j) + "_" + str(sel_x + i)).click()
                        mine_matrix[sel_y + j][sel_x +
                                               i] = minefield(sel_x + i, sel_y + j)
                        for m in range(-1, 2):
                            for n in range(-1, 2):
                                if not (m == 0 and n == 0):
                                    if sel_x + i + m != 0 and sel_x + i + m != w + 1 and sel_y + j + n != 0 and sel_y + j + n != h + 1:
                                        if mine_matrix[sel_y + j + n][sel_x + i + m] > 0:
                                            auxentios(sel_x + i + m,
                                                      sel_y + j + n)
                        if mine_matrix[sel_y + j][sel_x + i] == 0 and i != 0 and j != 0:
                            aristarchus(sel_x + i, sel_y + j,
                                        sel_x + i, sel_y + j)
                        elif mine_matrix[sel_y + j][sel_x + i] > 0:
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


def aristarchus(sel_x, sel_y, last_x, last_y):
    mine_matrix[sel_y][sel_x] = minefield(sel_x, sel_y)
    if mine_matrix[sel_y][sel_x] > -1:
        if mine_matrix[sel_y][sel_x] >= -2 and explored[sel_y][sel_x] != -1:
            # if mine_matrix[sel_y][sel_x] <= 0 and explored[sel_y][sel_x] != -1:
            if sel_x - last_x == 0 and sel_y - last_y == 0:
                change_face(sel_x, sel_y, (0, 0, 0, 0))
            else:
                find_face(sel_x, sel_y, last_x, last_y)
        explored[sel_y][sel_x] = -1

        if explored[sel_y][sel_x + 1] != -1:
            aristarchus(sel_x + 1, sel_y, sel_x, sel_y)
        if explored[sel_y + 1][sel_x] != -1:
            aristarchus(sel_x, sel_y + 1, sel_x, sel_y)
        if explored[sel_y][sel_x - 1] != -1:
            aristarchus(sel_x - 1, sel_y, sel_x, sel_y)
        if explored[sel_y - 1][sel_x] != -1:
            aristarchus(sel_x, sel_y - 1, sel_x, sel_y)

        if mine_matrix[sel_y][sel_x] > 0:
            auxentios(sel_x, sel_y)


def cleanup():
    for i in range(1, h + 1):
        for j in range(1, w + 1):
            if explored != 0:
                driver.execute_script(
                    "document.getElementById('" + str(i) + "_" + str(j) + "').style.backgroundPosition = ''")


link = ws_sizes[dificculty - 1][2]
faces = [[(0, 0, 0, 0) for _ in range(1, w + 2)] for _ in range(1, h + 2)]

skinMap = {
    'original': 'https://i.ibb.co/pRnqDqt/sprite100.gif',
    'roses' : 'https://i.ibb.co/h14qBg3/sprite100-roses.gif',
    'skin' : 'https://i.ibb.co/BCVtQ3x/sprite100-skinned.gif'
}

driver = webdriver.Chrome()
driver.get("https://minesweeperonline.com/" + link)
driver.execute_script(
    "var style = document.createElement('style'); style.type = 'text/css'; style.innerHTML = '.z100 #game div {background-image: url(" + skinMap[skin] + ");}'; document.getElementsByTagName('head')[0].appendChild(style);")

driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div[2]/div[2]/button[1]').click()

sel_x = randint(1, w)
sel_y = randint(1, h)

driver.find_element(By.ID, str(sel_y) + "_" +
                          str(sel_x)).click()
aristarchus(sel_x, sel_y, sel_x, sel_y)

while mines != ws_sizes[dificculty - 1][3]:
    driver.find_element(By.ID, "face").click()
    mines = 0
    sel_x = randint(1, w)
    sel_y = randint(1, h)
    mine_matrix = [[-1 for _ in range(w + 2)] for _ in range(h + 2)]
    explored = [[0 for _ in range(w + 2)] for _ in range(h + 2)]
    faces = [[(0, 0, 0, 0) for _ in range(1, w + 2)] for _ in range(1, h + 2)]
    cleanup()
    driver.find_element(By.ID, str(sel_y) + "_" +
                              str(sel_x)).click()
    aristarchus(sel_x, sel_y, sel_x, sel_y)
    # input()

WebDriverWait(driver, 3).until(EC.alert_is_present())
alert = driver.switch_to.alert()
alert.send_keys("WaVy")
alert.accept()


myfile = open("Times_Recursive_Efficient.txt", "a")
myfile.write("w:" + str(w) + " h:" + str(h) + " / " + str(driver.find_element(By.ID, "seconds_hundreds").get_attribute("class"))[4] + str(driver.find_element(By.ID, 
    "seconds_tens").get_attribute("class"))[4] + str(driver.find_element(By.ID, "seconds_ones").get_attribute("class"))[4] + "s\n")
myfile.close()

print("im done for whatever reason, i was called " + str(called) + " times.")

time.sleep(5)
