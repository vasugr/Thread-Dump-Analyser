
def getNext(slow, waiting,locked):
	if slow in waiting.keys():
		resid = waiting[slow]
	else:
		return None
	if resid in locked.keys():
		thinf2 = locked[resid]
	else:
		return None
	if thinf2 in waiting.keys():
		slow = thinf2
	else:
		return None
	return slow

def identifyDeadLock(locked,waiting):
	deadlockList = []
	found=False
	for tinfo,resourceID in waiting.items():
		if tinfo in deadlockList:
			continue
		slow = tinfo
		fast = tinfo
		while True:
			#fast
			next1 = getNext(fast,waiting,locked)
			if next1 is not None:
				next2  = getNext(next1,waiting,locked)
				if next2 is not None:
					fast = next2
				else:
					break
			else:
				break
			#slow
			next1 = getNext(slow,waiting,locked)
			if next1 is not None:
				slow = next1
			else:
				break
			if slow.tid == fast.tid:
				found=True
				break

		if found==True:
			finder = tinfo
			while finder.tid != slow.tid:
				deadlockList.append(finder)
				next1 = getNext(finder,waiting,locked)
				if next1 is not None:
					finder=next1	
				next2 = getNext(slow,waiting,locked)
				if next2 is not None:
					slow=next2
			deadlockList.append(finder)
			next1 = getNext(finder,waiting,locked)
			if next1 is not None:
				finder=next1
			while finder.tid != slow.tid:
				deadlockList.append(finder)
				next1 = getNext(finder,waiting,locked)
				if next1 is not None:
					finder=next1	
	return deadlockList







