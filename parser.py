import re
from .models import ThreadInfo

def toString(tinfo):
	ans=""
	ans = ans + tinfo.threadName + "\n"
	ans = ans + str(tinfo.daemon) + "\n"
	ans = ans + tinfo.priority + "\n"
	ans = ans + tinfo.osPriority + "\n"
	ans = ans + tinfo.tid + "\n"
	ans = ans + tinfo.nid + "\n"
	ans = ans + tinfo.state + "\n"
	ans = ans + tinfo.stackTrace + "\n"
	return ans

def listToString(tlist):
	ans ="" + "\n\n total threads ==   "+str(len(tlist))+"\n\n"
	for x in tlist:
		ans = ans+ toString(x) 
	return ans

def parseDump(thrdDump):
	tinfo = ThreadInfo.ThreadInfo()
	tinfoList = []
	namePattern ="^\"(.*)\"(.*)prio=([0-9]+) os_prio=([0-9]+) tid=(\\w*) nid=(\\w*)\\s\\w*"
	statePattern = "\\s+java.lang.Thread.State: (.*)"
	lockedPattern = "\\s+- locked\\s+<(.*)>\\s+\\(.*\\)"
	lockWaitPattern = "\\s+- parking to wait for\\s+<(.*)>\\s+\\(.*\\)"
	functionCallPattern = "\\s+at (.*)"
	stackTrace=""
	for line in thrdDump.splitlines():
		if( len(line) ==0):
			continue
		if(line[0]=='"'):
			if len(tinfo.state)>0:
				#stackTrace = stackTrace+"\n>>len = "+str(len(stackTrace))
				#tinfo.stackTrace = stackTrace
				if len(tinfo.stackTrace)>0:
					tinfoList.append(tinfo)
				tinfo = ThreadInfo.ThreadInfo()
				#stackTrace=""

			a=re.search(namePattern,line)
			#print(a.group(1))
			if a is None:
				continue
			tinfo = ThreadInfo.ThreadInfo()
			tinfo.threadName=str(a.group(1))
			tinfo.daemon= "daemon" in str(a.group(2))
			tinfo.priority = a.group(3)
			tinfo.osPriority= a.group(4)
			tinfo.tid=a.group(5)
			tinfo.nid=a.group(6)
			#return toString(tinfo)
		elif("Thread.State:" in line):
			a=re.search(statePattern,line)
			if a is None:
				continue
			tinfo.state = a.group(1).split()[0]
		elif(re.search(lockedPattern,line)):
			tinfo.stackTrace = tinfo.stackTrace+ "\t" + line + "\n"
			a = re.search(lockedPattern,line)
			if a is None:
				continue
			tinfo.locked.append(a.group(1))
		elif(re.search(lockWaitPattern,line)):
			tinfo.stackTrace = tinfo.stackTrace+ "\t" +line + "\n"
			a = re.search(lockWaitPattern,line)
			if a is None:
				continue
			tinfo.waiting.append(a.group(1))
		elif(re.search(functionCallPattern,line)):
			tinfo.stackTrace = tinfo.stackTrace+ "\t" +line + "\n"
			a = re.search(functionCallPattern,line)
			if a is None:
				continue
			tinfo.callList.insert(0,a.group(1))

	if(len(tinfo.threadName)>0 ):
		#tinfo.stackTrace = stackTrace
		if len(tinfo.stackTrace)>0:
			tinfoList.append(tinfo)

	return tinfoList


