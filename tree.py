import copy

class TreeNode:
  def __init__(this):
    this.value = ""
    this.numChild=0
    this.children=[]
    this.lineNum=1

def insertNode(root,func):
  if root.value == func:
    root.numChild+=1
    return root
  else:
    ans=None
    for child in root.children:
      ans = insertNode(child,func)
      if ans is not None:
        break
    return ans

def fillTree(root,tlist):
  for tinfo in tlist:
    root2=copy.copy(root)
    for func in tinfo.callList:
      node = insertNode(root2,func)
      if node is None:
        newnode = TreeNode()
        newnode.value = func
        root2.children.append(newnode)
        root2=newnode
      else:
        root2 =node

def printTree(root,indent):
  ans=""
  ans += "("+str(root.numChild)+")"+ root.value+"\n"
  treeFold = []
  tmpFold = []
  startoffoldret = len(ans)
  startoffold = len(ans)

  for child in root.children:
    startoffold = len(ans)
    ans+= indent+"|\n"+indent+"|----"
    indent2 = copy.copy(indent) + "\t"
    tmpans, _t,startoffold2 = printTree(child,indent2)
    ans += tmpans
    if indent == "\t\t":
      tmpFold.append(startoffold2+startoffold)
      tmpFold.append(len(ans)-2)
      treeFold.append(tmpFold)
      tmpFold = []
      

  return ans,treeFold, startoffoldret