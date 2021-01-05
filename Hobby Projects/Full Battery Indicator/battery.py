import psutil
from playsound import playsound

while True:
	bat=psutil.sensors_battery()
	per=int(bat.percent)
	if per==100:
		playsound('C:/Users/Bala/Desktop/tets.mp3')
		break