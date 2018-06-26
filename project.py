import random
# import matplotlib
# import matplotlib.pyplot as plt

def read_value(filename):
    with open(filename, 'r') as f:
        mode = f.readline()
        return mode
def read_data(filename):
    l = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            l.append(float(line.strip()))
        return l

def update_clock(master_clock,time):
    master_clock.append(time)
    new_list = sorted(master_clock)
    return new_list
    
def processing(arrival,service,para,number):
    m = int(para[0])
    setup_time = float(para[1])
    T = float(para[2])
    if len(para) ==4:
        time_end = para[3]
    server_state = ["OFF" for i in range(m)]
    master_clock = []
    master_clock += arrival
    complete_time = [-1 for j in range(m)]
    dispatcher = []
    departure= []
    while master_clock:
        current_time = master_clock[0]
#        print(dispatcher)
#        print("The time is " + str(current_time))
        if current_time in arrival:
            if "DELAYEDOFF" in server_state:
                max_value = -1
                for i in range(m):
                    if server_state[i] == "DELAYEDOFF":
                        index = server_state.index("DELAYEDOFF")
                        value = complete_time[index]
                        max_value = max(max_value,value)
                location = complete_time.index(max_value)
                server_state[location] = "BUSY"
                indx = master_clock.index(max_value)
                master_clock.pop(indx)
                ind = arrival.index(current_time)
                server_time = service[ind]
                complete_time[location] = current_time + server_time
                departure.append(complete_time[location])
#                print(server_state)
#                print(complete_time)
                master_clock.pop(0)
                master_clock = update_clock(master_clock,complete_time[location])
                
            elif "OFF" in server_state:
                index = arrival.index(current_time)
                server_time = service[index]
                flag = [current_time,server_time,"MARKED"]
                dispatcher.append(flag)
                index = server_state.index("OFF")
                server_state[index] = "SETUP"
                complete_time[index]= current_time + setup_time
                master_clock.pop(0)
                master_clock = update_clock(master_clock,complete_time[index])
#                print(server_state)
#                print(complete_time)
            else:
                index = arrival.index(current_time)
                server_time = service[index]
                flag = [current_time,server_time,"UNMARKED"]
                dispatcher.append(flag)
                master_clock.pop(0)
        else:
            index = complete_time.index(current_time)
            if server_state[index] == "SETUP":
                server_state[index] = "BUSY"
                complete_time[index] = current_time + dispatcher[0][1]
                departure.append(complete_time[index])
                master_clock.pop(0)
                master_clock = update_clock(master_clock,complete_time[index])
                dispatcher.pop(0)
#                print(server_state)
#                print(complete_time)
            elif server_state[index] == "BUSY":
                if len(dispatcher) == 0:
                    server_state[index] = "DELAYEDOFF"
                    complete_time[index] = current_time + T
                    master_clock.pop(0)
                    master_clock = update_clock(master_clock,complete_time[index])
                else:
                    unmarked_exist = False
                    for i in range(len(dispatcher)):
                        if dispatcher[i][2] == "UNMARKED":
                            unmarked_exist = True
                            dispatcher[i][2] = "MARKED"
#                            print(dispatcher)
                            break
                    if unmarked_exist == False:
                        max_value = -1
                        for j in range(m):
                            if server_state[j]=="SETUP":
                                value = complete_time[j]
                                if value >= max_value:
                                    max_value = value
                                    cnt = j
                        server_state[cnt] = "OFF"
                        complete_time[cnt] = -1
                        ind = master_clock.index(max_value)
                        master_clock.pop(ind)
                    complete_time[index] = current_time + dispatcher[0][1]
                    departure.append(complete_time[index])
                    master_clock.pop(0)
                    master_clock = update_clock(master_clock,complete_time[index])
                    dispatcher.pop(0)
#                print(server_state)
#                print(complete_time)
            elif server_state[index] == "DELAYEDOFF":
                server_state[index] = "OFF"
                ind = master_clock.index(current_time)
                master_clock.pop(ind)
                complete_time[index] = -1
#                print(server_state)
#                print(complete_time)
#    print(departure)
    if len(para) ==4:
        for k in range(len(departure)):
            if departure[k] > time_end:
                departure = departure[:k]
                arrival = arrival[:k]
                break
    mrt = (sum(departure)-sum(arrival))/len(departure)
    with open("mrt_" + str(number) + ".txt", "w") as file:
        file.write(str('%0.3f'%mrt))
    new_dic = {}
    for i in range(len(arrival)):
        if arrival[i] not in new_dic:
            new_dic[arrival[i]]= departure[i]
    new_list = list(sorted(new_dic.items(), key=lambda d:d[1]))
    with open("departure_" + str(number) + ".txt", "w") as f:
        for j in range(len(new_list)):
            f.write(str('%0.3f'%new_list[j][0])+ "\t" + str('%0.3f'%new_list[j][1]) + "\n")

                            
def main(arrival_name,service_name,para_name,mode_name,number):
    mode = read_value(mode_name)
    random.seed(1)
    if mode =="trace":
        arrival = read_data(arrival_name)
        service = read_data(service_name)
        para = read_data(para_name)
        processing(arrival, service,para,number)
    if mode == "random":
        lambda_value = float(read_value(arrival_name))
        mu_value = float(read_value(service_name))
        para = read_data(para_name)
        end_time = para[3]
        arrival = []
        service = []
        curr = 0
        flag = True
        while flag == True:
            inter = random.expovariate(lambda_value)
            curr += inter
            if curr < end_time:
                arrival.append(curr)
            else:
                flag = False
        job_number = len(arrival)
        for i in range(job_number):
            t = 0
            for j in range(3):
                t += random.expovariate(mu_value)
            service.append(t)
        processing(arrival, service,para,number)

    
    

        
