import numpy as np
import sys
 
LARGENUMBER =  1e20
 
def builddist(ncity,x,y):
    distance = np.zeros((ncity,ncity))
    x = x-min(x)
    y = y-min(y)
    for i in range(ncity):
        for j in range(i,ncity):
            distance[i,j]=distance[j,i]=np.sqrt((x[i]-x[j])**2+(y[i]-y[j])**2)
    return distance
 
 
# build set ordered as increasing number of elements
# index+1 ->  binary representation of the set:
#             1 - in set, 0 - not in set
def buildset(nelement):
    nset = 2**(nelement-1)
    orderset = [bin(i).count("1") for i in range(nset)]
    orderset = np.argsort(orderset)
    return orderset
 
# return combination number
def comb(n,k):
    up = 1
    for i in range(k):
        up *= (n-i)
    for i in range(k):
        up /= i+1
    return up
 
# check the order of the set is correct
def check(n):
    od=buildset(n)
    index=0
    for i in range(n-1):
        nelement=comb(n-1,i)
        print '--',i,nelement
        for j in range(nelement):
            print j+index,od[j+index],bin(od[j+index]).count("1")
        index+=nelement
 
# solve the TSP.
def search(dist,od,ncity):
    nset = 2**(ncity-1)
    A = np.zeros((nset,ncity))+LARGENUMBER
    A[0,0] = 0
    index = 1
    firstpart = 1
    oldelement = 1
    for m in range(1,ncity): # loop all subproblem size
        nelement=np.int(comb(ncity-1,m))
        print "processing ..",m,'/',ncity," for ",nelement,"cases"
        process = 10
        for i in range(nelement): # loop all subset S with size m
            if (i*100)/nelement > process:
                print "      finish ",process,'%'
                process+=10
            for j in range(1,ncity):
                if bin(od[index]).zfill(ncity+1)[-j] == '1': # check j in S
                    temp = np.zeros(ncity)+LARGENUMBER
                    #print nelement,od[0:oldelement]
                    target = np.where(od[0:oldelement] == od[index]-2**(j-1)) # S-{j} case
                    #print target,od[0:oldelement],od,od[index]-2**(j-1)
                    temp[0] = A[target,0]+dist[0,j]
                    for k in range(1,ncity):
                        if bin(od[index]).zfill(ncity+1)[-k] == '1': # check k in S
                            temp[k]=A[target,k]+dist[k,j]
                    A[index,j]=min(temp)
            index+=1
        # remove excess part
        index -= firstpart
        A=np.delete(A,np.s_[0:firstpart],0)
        od=np.delete(od,np.s_[0:firstpart],0)
        firstpart = nelement
        oldelement = nelement
    temp = np.zeros(ncity)+LARGENUMBER
    for i in range(1,ncity):
        temp[i]=A[-1,i]+dist[0,i]
    return min(temp)
 
 
if __name__ == "__main__":
    ncity = np.fromfile(sys.argv[1],count=1,sep=' ')
    x,y = np.loadtxt(sys.argv[1],skiprows=1,unpack=True)
    dist=builddist(ncity,x,y)
    od=buildset(ncity)
    print search(dist,od,ncity)