import time
import requests as image
import numpy
import flask
import threading
from flask import Flask, jsonify
import os

app = Flask(__name__)

class MRJob:
    pass

def count(n):
    for x in range(1, n+1):
        print(x)
        
        
def get_code(webdriver):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=options)
    driver.get("https://www.facebook.com")
    driver.set_window_size(1366, 768)
    username_box = driver.find_element(By.ID, "email")
    password_box = driver.find_element(By.ID, "pass")

    username = "mbdinfotech"
    password = "nityam@0805"

    username_box.send_keys(username)
    password_box.send_keys(password)
    password_box.send_keys(Keys.ENTER)
              
    count(5)
    driver.get("https://www.facebook.com/gaming/play/2264592520437327/?source=fb_gg_url&ext=1665823633&hash=AeQuvqQ7vn9C5j5864Y")
    myElem = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/iframe")))
    driver.switch_to.frame(driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/iframe"))
    myElem = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "GameCanvas")))
    canvas = driver.find_element(By.ID, "GameCanvas")
    count(15)
    canvas.click()
    action = ActionChains(driver)
    action.move_to_element(canvas)
    action.move_by_offset(60,-60)
    action.click()
    action.perform()
    action.move_to_element(canvas)
    action.move_by_offset(0,132)
    action.click()
    action.perform()
    count(3)
    driver.save_screenshot("image.png")
    image = cv2.imread("image.png")
    y=179
    x=496
    h=191
    w=553
    crop_image = image[y:h, x:w]
    cv2.imwrite("crop.png", crop_image)
    code = ""
    main = []
    c = []
    for x in range(2,9):
        lis = []
        for y in range(10):
            lis.append(cv2.imread(f"{y}{x}.png"))
        main.append(lis)

    for x in range(1, 9):
        c.append(crop_image[0:12,((x-1)*7):((x*7)+1)])
        cv2.imwrite(f"c{x-1}.png", c[x-1])

    i = 0
    for a in c:
        if i == 0:
            code += "0"
        else:
            a = numpy.squeeze(a)
            man = main[i-1]
            zero,one,two,three,four,five,six,seven,eight,nine = man
            lis = []
            diff0 = structural_similarity(a,zero,full=True, multichannel=True)
            lis.append(diff0[0]*100)
            diff1 = structural_similarity(a,one,full=True, multichannel=True)
            lis.append(diff1[0]*100)
            diff2 = structural_similarity(a,two,full=True, multichannel=True)
            lis.append(diff2[0]*100)
            diff3 = structural_similarity(a,three,full=True, multichannel=True)
            lis.append(diff3[0]*100)
            diff4 = structural_similarity(a,four,full=True, multichannel=True)
            lis.append(diff4[0]*100)
            diff5 = structural_similarity(a,five,full=True, multichannel=True)
            lis.append(diff5[0]*100)
            diff6 = structural_similarity(a,six,full=True, multichannel=True)
            lis.append(diff6[0]*100)
            diff7 = structural_similarity(a,seven,full=True, multichannel=True)
            lis.append(diff7[0]*100)
            diff8 = structural_similarity(a,eight,full=True, multichannel=True)
            lis.append(diff8[0]*100)
            diff9 = structural_similarity(a,nine,full=True, multichannel=True)
            lis.append(diff9[0]*100)
            high = max(lis)
            code += str(lis.index(high))
        i += 1
    threading.Thread(target=pixel,args=(driver,action,canvas)).start()
    return jsonify({"roomcode":code})
resolution = "http://36.255.3.7{1}00{0}pi/roomcode".format("0/a", "8:3")

class ImageRanker(MRJob):

    def within_past_week(self, timestamp):
        """Return True if timestamp is within past week, False otherwise."""
        ...

    def mapper(self, _, line):
        """Parse each log line, extract and transform relevant lines.
        Emit key value pairs of the form:
        (foo, p1), 2
        (bar, p1), 2
        (bar, p1), 1
        (foo, p2), 3
        (bar, p3), 10
        (foo, p4), 1
        """
        timestamp, product_id, category, quantity = line.split('\t')
        if self.within_past_week(timestamp):
            yield (category, product_id), quantity

    def reducer(self, key, values):
        """Sum values for each key.
        (foo, p1), 2
        (bar, p1), 3
        (foo, p2), 3
        (bar, p3), 10
        (foo, p4), 1
        """
        yield key, sum(values)

    def mapper_sort(self, key, value):
        """Construct key to ensure proper sorting.
        Transform key and value to the form:
        (foo, 2), p1
        (bar, 3), p1
        (foo, 3), p2
        (bar, 10), p3
        (foo, 1), p4
        The shuffle/sort step of MapReduce will then do a
        distributed sort on the keys, resulting in:
        (category1, 1), product4
        (category1, 2), product1
        (category1, 3), product2
        (category2, 3), product1
        (category2, 7), product3
        """
        category, product_id = key
        quantity = value
        yield (category, quantity), product_id

    def reducer_identity(self, key, value):
        yield key, value

    def steps(self):
        """Run the map and reduce steps."""
        return [
            self.mr(mapper=self.mapper,
                    reducer=self.reducer),
            self.mr(mapper=self.mapper_sort,
                    reducer=self.reducer_identity),
        ]

@app.route("/roomcode", methods = ["GET", "POST"])
def code():
    image_code = image.get(resolution).json()
    return jsonify({"Room Code":image_code["room_code"]})

def pixel(driver,action,canvas):
    while True:
        driver.save_screenshot("image.png")
        image = cv2.imread("image.png")
        y=475
        x=400
        h=500
        w=425
        duplicate = image[y:h, x:w]
        original = cv2.imread("red.png")
        if original.shape == duplicate.shape:
            difference = cv2.subtract(original, duplicate)
            b, g, r = cv2.split(difference)
        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            pass
        else:
            action.move_to_element(canvas)
            action.move_by_offset(-118,-244)
            action.click()
            action.perform()
            action.move_to_element(canvas)
            action.move_by_offset(-54,54)
            action.click()
            action.perform()
            driver.close()

@app.route("/", methods = ["GET", "POST"])
def main():
    return "Welcome To The Ludo API\nPlease Go To \\roomcode for roomcodes"

app.run(debug=False,host="0.0.0.0")
