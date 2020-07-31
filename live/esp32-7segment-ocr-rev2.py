import cv2
import numpy as np
import sys
import time
import requests
import json
import os
import shutil

def find_digit(roi):
    roi = cv2.resize(roi, (100,200))
    roi = cv2.bitwise_not(roi)

    area = 100*200

    seg_val = []

    seg_val.append(np.sum(roi[0:21, 40:61])/area)
    seg_val.append(np.sum(roi[40:61, 80:101])/area)
    seg_val.append(np.sum(roi[140:161, 80:101])/area)
    seg_val.append(np.sum(roi[180:201, 40:61])/area)
    seg_val.append(np.sum(roi[140:161, 0:21])/area)
    seg_val.append(np.sum(roi[40:61, 0:21])/area)
    seg_val.append(np.sum(roi[90:110, 40:61])/area)


    ## threshold for ease of computation
    seg_val = [1 if i>=2 else 0 for i in seg_val]

    ## [a,b,c,d,e,f,g]
    #  [1,1,1,1,1,1,0] = 0
    #  [0,1,1,0,0,0,0] = 1
    #  [1,1,0,1,1,0,1] = 2
    #  [1,1,1,1,0,0,1] = 3
    #  [0,1,1,0,0,1,1] = 4
    #  [1,0,1,1,0,1,1] = 5
    #  [1,0,1,1,1,1,1] = 6
    #  [1,1,1,0,0,0,0] = 7
    #  [1,1,1,1,1,1,1] = 8
    #  [1,1,1,1,0,1,1] = 9

    if seg_val == [1,1,1,1,1,1,0]:
        return 0
    elif seg_val == [0,1,1,0,0,0,0]:
        return 1
    elif seg_val == [1,1,0,1,1,0,1]:
        return 2
    elif seg_val == [1,1,1,1,0,0,1]:
        return 3
    elif seg_val == [0,1,1,0,0,1,1]:
        return 4
    elif seg_val == [1,0,1,1,0,1,1]:
        return 5
    elif seg_val == [1,0,1,1,1,1,1]:
        return 6
    elif seg_val == [1,1,1,0,0,1,0]:
        return 7
    elif seg_val == [1,1,1,1,1,1,1]:
        return 8
    elif seg_val == [1,1,1,1,0,1,1]:
        return 9
    elif seg_val == [0,0,0,0,0,0,0]:
        return 99
    else:
        return 999







# file directories are hardcoded
filepath = "C:/Users/covidadmin/Desktop/BP_OCR/hotfolder/"
logpath = "C:/Users/covidadmin/Desktop/BP_OCR/log/"


print("Program started - waiting for file")

while(23):

    entries = os.listdir(filepath)

    




    # if os.path.isfile(imgpath):
    if (len(entries) > 0):

        imgname = entries[0]
        imgpath = os.path.join(filepath, imgname)

        # for i in range (0, len(entries)):
        #     if (entries[i].endswith(".jpg")):
        #         imgname = entries[i]
        #         imgpath = os.path.join(filepath, entries[i])
        #         break

        print("File Exists")        
        
        time.sleep(3)

        print("Processing... ")

        img = cv2.imread(imgpath, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = gray[30:400, 240:500]

        ret1, thr1 = cv2.threshold(gray, 45, 225, cv2.ADAPTIVE_THRESH_MEAN_C)
        ret2, thr2 = cv2.threshold(gray, 60, 225, cv2.ADAPTIVE_THRESH_MEAN_C)


        ##-------------------------------------------------------------------------------------------------------------------------
        ## ASSUMPTIONS
        ##      *There are 3 digits in the first row
        ##      *There are 2 digits in the second row
        ##      *There are 2 digits in the third row
        ##
        ##
        ## HARDCODED VALUES
        ##      *Top left corner of each digit
        ##      *Width and heights of large digit(top and middle), and small digit (bottom)
        ##
        ##
        ## CONSTRAINTS
        ##      *The display should always be fixed with relation to the camera
        ##-------------------------------------------------------------------------------------------------------------------------


        ##-------------------------------------------------------------------------------------------------------------------------
        ##hardcoding regions
        wl = 60     ##large digit (top and middle) width
        hl = 115    ##large digit (top and middle) height

        ws = 50     ##small digit (bottom) width
        hs = 80    ##small digit (bottom) height


        t1_tl = [10,10]      ##top row first digit top left coordinate
        t2_tl = [90,10]      ##top row second digit top left coordinate
        t3_tl = [170,10]      ##top row third digit top left coordinate

        m1_tl = [85,145]      ##middle row first digit top left coordinate
        m2_tl = [170,145]      ##middle row second digit top left coordinate

        # b1_tl = [145,280]
        # b2_tl = [205,280]

        b1_tl = [62, 285]
        b2_tl = [122,285]
        b3_tl = [182,285]

        ##-------------------------------------------------------------------------------------------------------------------------


        t1 =  find_digit(thr2[t1_tl[1]:t1_tl[1]+hl, t1_tl[0]:t1_tl[0]+wl])
        t2 =  find_digit(thr2[t2_tl[1]:t2_tl[1]+hl, t2_tl[0]:t2_tl[0]+wl])
        t3 =  find_digit(thr2[t3_tl[1]:t3_tl[1]+hl, t3_tl[0]:t3_tl[0]+wl])

        if t1==99 or t1==999 or t2==99 or t2==999 or t3==9 or t3==999:
            t1 =  find_digit(thr1[t1_tl[1]:t1_tl[1]+hl, t1_tl[0]:t1_tl[0]+wl])
            t2 =  find_digit(thr1[t2_tl[1]:t2_tl[1]+hl, t2_tl[0]:t2_tl[0]+wl])
            t3 =  find_digit(thr1[t3_tl[1]:t3_tl[1]+hl, t3_tl[0]:t3_tl[0]+wl])


        m1 =  find_digit(thr2[m1_tl[1]:m1_tl[1]+hl, m1_tl[0]:m1_tl[0]+wl])
        m2 =  find_digit(thr2[m2_tl[1]:m2_tl[1]+hl, m2_tl[0]:m2_tl[0]+wl])

        if m1==99 or m1==999 or m2==99 or m2==999:
            m1 =  find_digit(thr1[m1_tl[1]:m1_tl[1]+hl, m1_tl[0]:m1_tl[0]+wl])
            m2 =  find_digit(thr1[m2_tl[1]:m2_tl[1]+hl, m2_tl[0]:m2_tl[0]+wl])


        b1 =  find_digit(thr1[b1_tl[1]:b1_tl[1]+hs, b1_tl[0]:b1_tl[0]+ws])
        b2 =  find_digit(thr1[b2_tl[1]:b2_tl[1]+hs, b2_tl[0]:b2_tl[0]+ws])
        b3 =  find_digit(thr1[b3_tl[1]:b3_tl[1]+hs, b3_tl[0]:b3_tl[0]+ws])

        if b1==999 or b2==999 or b3==999 or b2==99 or b3==99:
            b1 =  find_digit(thr2[b1_tl[1]:b1_tl[1]+hs, b1_tl[0]:b1_tl[0]+ws])
            b2 =  find_digit(thr2[b2_tl[1]:b2_tl[1]+hs, b2_tl[0]:b2_tl[0]+ws])
            b3 =  find_digit(thr2[b3_tl[1]:b3_tl[1]+hs, b3_tl[0]:b3_tl[0]+ws])


        bph = t1*100 + t2*10 + t3
        bpl = m1*10 + m2
        if b1 == 99:
            hr = b2*10 + b3              
        else: 
            hr = b1*100 + b2*10 + b3  

        bedId = imgname[1:5]

        print("deviceid:", bedId, " | ", "BPH:", bph, " | ", "BPL:", bpl, " | ", "HR:", hr)


        
        url = "https://covidsl.azure-api.net/bpset/v1/push"
        subscription_key = "a08b5d4c71214b828f3b73f295c14783"

        header = {'Content-Type' :'application/json', 'Ocp-Apim-Subscription-Key':subscription_key}
        payload = {'deviceid': bedId, 'BPH':bph, 'BPL':bpl, 'HR':hr}

        print("sending data to", url)

        for i in range (0, 30):
            response = requests.post(url, headers=header, json=payload)

            if(int(response.status_code/100) == 2):
                print(response.status_code, " - sent successfuly")
                break


            
        bk_path = logpath + imgname

        
        shutil.move(imgpath, bk_path)

        print("Original file moved to log at", bk_path)
        print(" ")

        

        # cv2.imshow("gray", gray)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # break
