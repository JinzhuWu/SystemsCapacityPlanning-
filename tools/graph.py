import random  
import matplotlib  
import matplotlib.pyplot as plt
import numpy as np
time = []
arrival = []
departure = []
with open("mrt_3.txt","r") as file:
    t = float(file.readline())
with open("departure_3.txt","r") as f:
    for lines in f:
        time.append(lines.strip().split("\t"))
for i in range(len(time)):
    arrival.append(float(time[i][0]))
    departure.append(float(time[i][1]))
    
steady_mrt = (sum(departure[1600:]) - sum(arrival[1600:]))/(len(departure)-1600)
print(steady_mrt)

theoretical_mean = [t for i in range(len(time))]
mrt_list = []
for i in range(len(time)):
    mrt = (sum(departure[:i+1]) - sum(arrival[:i+1]))/(i+1)
    mrt_list.append(mrt)


x = np.arange(1,len(time)+1,1)
y = mrt_list
z = theoretical_mean
plt.figure()
plt.plot(x,y,label="Running mean")
plt.plot(x,z,label="Theoretical_mean")
plt.xlabel("K jobs")
plt.ylabel("Mean response time of first K jobs")
plt.title("Transient behaviour versus steady state behaviour")
plt.show()


