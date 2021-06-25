import time
import win32com.client
dehua = win32.com.client.Dispatch('SAPI.SPVOICE')

while True:
	dehua.speak('sunck is a handsome man')
	time.sleep(5)



