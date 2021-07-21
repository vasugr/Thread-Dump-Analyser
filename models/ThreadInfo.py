class ThreadInfo:
  def __init__(this):
    this.threadName = ""
    this.daemon=False
    this.priority=""
    this.osPriority=""
    this.tid=""
    this.nid=""
    this.state = ""
    this.stackTrace=""
    this.locked=[]
    this.waiting=[]
    this.callList=[]