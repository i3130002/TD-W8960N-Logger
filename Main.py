from AdslStatus import AdslStatus
import csv
import time,datetime



adslStatus = AdslStatus(isDebug=False)

with open('D:\D\project\Python\ADSL Status\out.csv',  'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f,)
    res = adslStatus.extractDataDeviceInfo()
    res["DateTime"] = str(datetime.datetime.now())
    writer.writerow(res.keys())

    while True:
        row = adslStatus.extractDataDeviceInfo()
        row["DateTime"] = str(datetime.datetime.now())
        row = row.values()
        writer.writerow(row)
        print("Done")
        time.sleep(1)



print("Done")