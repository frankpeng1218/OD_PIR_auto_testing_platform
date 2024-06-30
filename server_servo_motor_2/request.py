
import time
import network
import urequests as requests

ssid = 'frank0820_2.4G'
password = 'jotao1218'

wlan = network.WLAN(network.STA_IF)

#function to connect to Wi-Fi network
def cnctWifi():
    
    wlan.active(True)
    wlan.connect(ssid, password)
    
    # Wait for connection to establish
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
                break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
    
    # Manage connection errors
    if wlan.status() != 3:
        print('Network Connection has failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )

#function to send http get request
def getData():
    try:
        data=requests.get("http://192.168.15.100:5000")
        print(data.text)


    except:
        print("could not connect (status =" + str(wlan.status()) + ")")

cnctWifi() 
   
while True:
    if wlan.isconnected():
        print("sending get request...")
        getData()
    else:
        print("attempting to reconnect...")
        wlan.disconnect()
        cnctWifi()
    time.sleep(1)
