import project as project

with open("num_tests.txt","r") as file:
    number = int(file.readline())
for i in range(number):
    arrival_name = "arrival_" + str(i+1) + ".txt"
    service_name = "service_" + str(i+1) + ".txt"
    para_name = "para_" + str(i+1) + ".txt"
    mode_name = "mode_" + str(i+1) + ".txt"
    project.main(arrival_name,service_name,para_name,mode_name,i+1)
