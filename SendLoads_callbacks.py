import subprocess as sp
import pyads
import time
import csv
import array as arr
from ctypes import sizeof

# testing code
# how does it look
#Init
#this is me
lsDLC=[]
lsTimeStep=[]
RigForce1=[]
lsRigForce2=[]
lsRigForce3=[]
bStart=1
bInterrupt=None
nState=0


if nState==0:
        sFilePath="C:\svn-sandbox\AR1500-Control\Scripts\PythonADS\sin_load_35kN_1sec.csv"
elif nState==2:
        sFilePath = plc.read_by_name('.sFilePath',pyads.PLCTYPE_STRING)
        time.sleep(0.2)                


plc = pyads.Connection('5.78.127.52.1.1', pyads.PORT_SPS1)
plc.open()
bConnected = plc.read_by_name('.g_bConnectADSStream',pyads.PLCTYPE_BOOL)
reader =csv.reader(open(sFilePath,"rb"), delimiter=',')
next(reader,None) #skip the headers

#request callback function
@plc.notification(pyads.PLCTYPE_INT)
def callback(handle, name, timestamp, value):
	global bInterrupt
	print(
		'{0}: received new notitifiction for variable "{1}", value: {2}'
		.format(name, timestamp, value) 
	)
	bInterrupt = 1

# Add notification with default settings
plc.add_device_notification('.iCtrl', pyads.NotificationAttrib(2),
                                callback)
#print bInterrupt

while(bConnected):
	
	#read the status of start streaming
	print time.clock()
	#bStart = plc.read_by_name('.bStart',pyads.PLCTYPE_BOOL)
	print "Connected to PLC"
	#print time.clock()
	#Interrupt the data stream
	if nState==1 and not bInterrupt :
			for row in reader:
			   print bInterrupt,
			   if bInterrupt:
			   		break
			   print time.clock()
			   rRigForce1 = float(row[3])
			   rRigForce2 = float(row[4])
			   rRigForce3 = float(row[5])
			   rPitchAngle= float(row[1])
			   rTime = float(row[0])
			   a = arr.array('f', [rTime, rPitchAngle, rRigForce1,rRigForce2,rRigForce3])
			   plc.write_by_name('.arrTest',a,pyads.PLCTYPE_ARR_REAL(5))
			   print(rTime, rPitchAngle, rRigForce1, rRigForce2, rRigForce2, sFilePath),
			   time.sleep(0.01)
			   print(time.clock())
			   #sp.call("cls", shell=True)
	else:
		nState = plc.read_by_name('.iCtrl',pyads.PLCTYPE_INT)
		bInterrupt=0

		if nState==2:  
				#load csv
				sFilePath = plc.read_by_name('.sFilePath',pyads.PLCTYPE_STRING)
				reader =csv.reader(open(sFilePath,"rb"), delimiter=',')
				next(reader,None) #skip the headers
                                plc.write_by_name('.sFilePathRcv',sFilePath,pyads.PLCTYPE_STRING);
			
