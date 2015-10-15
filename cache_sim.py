"""
This project is done by S M Azharul Karim, student ID: dhf227,
for the course EE 5123-Computer architecture.

this is a cache simulator. it reads configuration from a text file called:
example.cfg and memory traces from another one called: example:trc. 
"""
import math

#read input file and converting the values accordingly
f1=open('example.trc','r')
f2=open('example1.cfg','r')

str1=[]
str2=[]
cache_size=0
block=0
seta=0
hit=0
miss=0
num1=[]
i=0

# reading trace file
for line in f1:
    str1.append(line[2:10])
    num1.append(bin(int(str1[i],16))[2:].zfill(32))
    i=i+1

N=len(str1)

#reading config file
for line in f2:
    str2.append(line)

temp1=str2[0]
temp2=str2[1]
temp3=str2[2]
cache_size=int(temp1[11:len(temp1)],10)
block=int(temp2[11:len(temp2)],10)
set_ass=int(temp3[14],10)
set_ass=int(set_ass)

# calculating block offset, tag, index, set
tag=0
index=0
block_offset=0
block_adds=0
index=math.log((cache_size/(block*set_ass)), 2)
index=int(index)
block_offset=math.log(block,2)
block_offset=int(block_offset)
block_adds=32-block_offset
tag=block_adds-index
tag=int(tag)
set_no=2**index
set_no=int(set_no)

# defining cache and count
cache=[[0 for x in range(set_ass)] for x in range(set_no)]
row=len(cache)
col=len(cache[0])
count=[[0 for x in range(set_ass)] for x in range(set_no)]

# the below for loop does everything a cache with LRU does
for i in range(N):
    for p in range(row):
            for q in range(col):
                # incrementing all non-zero trace values of count by 1
                # each time we access a new trace
                if int(str(cache[p][q]),2)!=0:
                    count[p][q]=count[p][q]+1
    temp=num1[i]
    # set is the row number, 
    set_int=int(temp[tag:(tag+index-1)],2)
    for j in range(set_ass):
    
        # when there are values in cache and there is a hit
        if int(str(cache[set_int][j]),2)!=0:
            temp2=cache[set_int][j]
            if temp[0:tag+index-1]==temp2[0:tag+index-1]:
                  hit=hit+1
                  # when we have got one matching value, setting the count
                  # of that value=0, LRU logic
                  count[set_int][j]=0
                  
        # when there are values in cache and there is a miss
            else:
                miss=miss+1
                max_count=max(count[set_int])
                temp_col=0
                temp_row=0
                for q in range(col):
                    if count[set_int][q]==max_count:
                        temp_col=q
                    break
                cache[set_int][temp_col]=num1[i]
            break         
            
        # when there are no values in cache, put values in cache
        # based on the relative set no and column, at the begining
        elif cache[set_int][j]==0:
            miss=miss+1
            cache[set_int][j]=num1[i]
            # when we have got one matching value, setting the count
            # of that value=0, LRU logic
            count[set_int][j]=0
        break

hit_rate=float(hit)/float(N)
print "tag length=", tag
print "index length=", index
print "offset length=",block_offset
print "no of address accessed=",N
print "no of hits=", hit
print "no of misses=", miss
print "cache hit rate=",hit_rate 
