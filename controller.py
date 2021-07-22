from . import parser
from . import analyzer
from . import deadlock
from . import tree
import os
import sublime

def generateStringSummary(analyzed):
	ans = ""
	ans1 = "\n -------------------------------------------------\n";
	ans1+= "|\tTHREAD DUMP SUMMARY :\n";

	ans2 = " -------------------------------------------------\n";
	ans2+= "|  THREAD COUNT SUMMARY: \n";

	ans3 = "\n -------------------------------------------------\n";
	ans3+= "|  DEADLOCKS DETECTED: \n";

	ans4 = "\n -------------------------------------------------\n";
	ans4+= "|  BOTTOM UP CALL STACK TREE: \n\n";

	ans5 = "\n -------------------------------------------------\n";
	ans5+= "|  TEST FUNCTION ORDER: \n\n";

	totThrdCount=0
	numDaemon=0

	#string/resourceID to tinfo 
	lockedDic = {}
	#tinfo to string/resourceID
	waitingDic = {}
	deadlocks=[]

	root = tree.TreeNode()
	root.value = "\troot"
	stacktraceFold = []
	treeFold = []
	root.lineNum=1
	#print("type of anal  = "+ str(type(analyzed)))
	for state,straceDict in analyzed.items():
		ans1 += " -------------------------------------------------\n"
		ans1 += "|\t\tSTATE : "+state+"\n"
		ans1 += "  ------------------------------------------------\n\n"

		tmpstraceRegion2 = []
		tmpstraceRegion2.append(len(ans1)-53)
		
		thrdStateCount=0

		if state == "BLOCKED":
			for strace,thrdList in straceDict.items():
				for tinfo in thrdList:
					for locked in tinfo.locked:
						lockedDic[locked]=tinfo
			for strace,thrdList in straceDict.items():
				for tinfo in thrdList:
					for waiting in tinfo.waiting:
						if waiting in lockedDic.keys():
							waitingDic[tinfo]=waiting
			deadlocks = deadlock.identifyDeadLock(lockedDic,waitingDic)

		for strace, thrdList in straceDict.items():
			numDaemon += sum(p.daemon==True for p in thrdList)
			numThrds = len(thrdList)
			thrdStateCount+=numThrds

			ans1 += "\t"
			if numThrds>1 :
				ans1+= str(numThrds)+" THREADS with "
			else:
				ans1+= "1 THREAD with"

			thrdNameList =  [t.threadName for t in thrdList]
			sharedStart = os.path.commonprefix(thrdNameList)

			ans1+= "THREAD NAME : " + sharedStart + "\n"
			tmpstraceRegion = []
			tmpstraceRegion.append(len(ans1)-1)
			ans1+= strace + "\n"
			tmpstraceRegion.append(len(ans1)-2)
			stacktraceFold.append(tmpstraceRegion)
			tree.fillTree(root,thrdList)
			#for tinfo in thrdList:
			#	ans5 += "\n -------------------------------------------------\n"
			#	ans5 += ' '.join(map(str, tinfo.callList)) 

		tmpstraceRegion2.append(len(ans1)-2)

		print(" start = "+str(tmpstraceRegion2[0]) + " end = " + str(tmpstraceRegion2[1]))

		stacktraceFold.append(tmpstraceRegion2)

		ans2 += "\n\t\t"+state + " : " + str(thrdStateCount)
		totThrdCount+=thrdStateCount

	ans2+="\n\tTOTAL THREADS COUNT = "+str(totThrdCount)
	ans2 += "\n -------------------------------------------------\n"
	ans2+= "|  DAEMON VS NON-DAEMON : \n";
	ans2+= "\n\t\t DAEMON : "+str(numDaemon)
	ans2+= "\n\t\t NON-DAEMON : "+str(totThrdCount-numDaemon) + "\n"

	ans += ans2
	#deadlock
	if len(deadlocks)==0:
		ans3+="\n\t\tNONE\n"
	else:
		for tinfo in deadlocks:
			ans3+= "\n   THREAD NAME : "+tinfo.threadName
			ans3+= "\n"+tinfo.stackTrace

	ans3 += "\n -------------------------------------------------\n"
	ans+=ans3

	tmpans4,treeFold,_e = tree.printTree(root,"\t\t")

	regionOffset = len(ans) + len(ans4)+10

	treefold2 = [sublime.Region(a[0]+regionOffset,a[1]+regionOffset-9) for a in treeFold]

	ans4 += str(tmpans4)
	ans4 += "\n -------------------------------------------------\n"
	ans += ans4

	regionOffset = len(ans)
	stacktraceFold2 = [sublime.Region(a[0]+regionOffset,a[1]+regionOffset) for a in stacktraceFold]

	print(" offset = "+str(regionOffset))

	ans += ans1

	return ans,stacktraceFold2+treefold2
		

def generateSummary(thrdDump):
	#print("generating sumary...\n")
	parsed = parser.parseDump(thrdDump)
	#print("parsed....\n")
	analyzed = analyzer.AnalyzeDump(parsed)
	#print("analyzed ... \n")
	return generateStringSummary(analyzed)
	#return str(analyzed.keys())