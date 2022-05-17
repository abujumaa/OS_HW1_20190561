import sys
ins = sys.argv
quant = 0
t = 0
timeline = []
fn = ins[1]
schalg = ins[2]
if(schalg == "RR"):
  quant = ins[3]
quantum = int(quant)

def modlines(): #100%
  line = []
  with open(fn, "r") as file:
    line = file.readlines()
    line = [line.replace('\n', '') for line in line]
    for i in range(len(line)):
      line[i] = line[i].split(' ')
  return line

def modpro(): #100%
  line = []
  pr = []
  idletl = []
  it = 0
  line = modlines()
  id = 1
  for i in range(len(line)):
    if line[i][0] == 'proc':
      line[i].append(str(it))
      line[i].append(str(id))
      pr.append(line[i]) 
      idletl.append(it)
      id += 1
    if line[i][0] == 'idle':
      it += int(line[i][1])
    if line[i][0] == 'Done':
      break
  return pr, idletl

def RR(quantum):
  tl = []
  ids = []
  tl.append(0)
  ids.append(1)
  pro = []
  at = [] #ARRIVAL TIME 'id-1'
  bt = [] #BURST TIME 'id-1'
  temp = []
  pro, at = modpro()
  n = len(pro) 
  tempn = n
  flag = 0 #FLAG
  # wt = 0 #WAITING TIME
  tat = 0 #TURNAROUND TIME
  rt = 0 #RESPONSE TIME
  totalbt = 0 #TOTAL BURST TIME
  for i in range(len(pro)):
    bt.append(int(pro[i][2]))
  for i in range(n):
    temp.append(bt[i]) #TO WORK ON TEMP
  i = 0
  while (tempn != 0): 
    if(temp[i] <= quantum and temp[i] > 0):
      totalbt += temp[i]
      temp[i] = 0
      flag = 1
    elif(temp[i] > 0):
      temp[i] -= quantum
      totalbt += quantum
    if(temp[i] == 0 and flag == 1):
      tempn -= 1
      tat = tat + totalbt - at[i]  
      flag = 0 
    if(i == n - 1):
      i = 0
    elif(at[i + 1] <= totalbt):
      i += 1
    else:
      i = 0
    tl.append(totalbt)
    if (i+1) not in ids:
      rt += tl[i] 
    ids.append(i + 1)
  tl = list(set(tl))
  tl.sort()
  atat = tat / n #Avg. TURNAROUND TIME
  art = rt / n #Avg. RESPONSE TIME
  return atat, art, tl, ids
  
def PR():
  tl = []
  tl.append(0)
  pro = []
  at = []
  pro, at = modpro()
  n = len(pro)
  bt = []
  rt = []
  for i in range(n):
    bt.append(int(pro[i][2]))
  wt = [0] * n
  tat = [0] * n
  sumt = 0
  sumr = 0
  temp = [0] * n
  temp[0] = 0
  wt[0] = 0
  for i in range(1, n):
    temp[i] = bt[i-1] + temp[i - 1]
    wt[i] = temp[i] - at[i]
    if(wt[i] < 0):    
      wt[i] = 0
  for i in range(n):
    tat[i] = wt[i] + bt[i]
  stime = [0] * n
  ctime = [0] * n
  stime[0] = 1
  ctime[0] = stime[0] + tat[0]
  for i in range(1, n):
    stime[i] = ctime[i - 1]
    ctime[i] = stime[i] + tat[i] - wt[i]
  for i in range(len(stime)):
    stime[i] -= 1
  for i in range(len(ctime)):
    ctime[i] -= 1
  for i in range(n):
    rt.append(stime[i] - int(at[i]))
  for i in range(n):
    sumt += tat[i]
    sumr += rt[i]
  for i in range(len(stime)):
    tl.append(stime[i])
    tl.append(ctime[i])
  tl = list(set(tl))
  tl.sort()
  pro = sorted(pro, key = lambda x:x[1])
  pro = sorted(pro)
  atat = sumt / n
  art = sumr / n
  ids = []
  for i in range(len(pro)):
    ids.append(pro[i][4])
  return atat, art, tl, ids
       
# OUTPUT
print("Input File Name:\t", fn)
if(schalg == "PR"):
  print("CPU Scheduling Algorithm:", schalg)
  atat, art, tl, id = PR()
elif(schalg == "RR"):
  print("CPU Scheduling Algorithm:", schalg, "(%s)" %quant)
  atat, art, tl, id = RR(quantum)
print("Avg. Turnaround time:\t", atat)
print("Avg. Response time:\t", art)
print("Timeline:")
for i in range(len(tl) - 1):
  print(int(id[i]), ":\t", int(tl[i]), " -> ", int(tl[i+1]))
