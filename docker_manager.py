import docker

#initialize docker
client = docker.from_env()
l = client.containers.list()


networks = ['web1', 'web2', 'web3', 'web4', 'web5']
active_containers = []
active_master=[]


class MyContainer():
    """
    To contain necessary information about Docker Containers for testing
    """
    service_name=None
    container=None


    def __init__(self, container):
        self.container=container
        self.service_name=self.__get_service_name()

    def set_status(self, status):
            status

    def get_id(self, ):
        return self.container.attrs['Config']['Hostname']

    def get_name(self, ):
        return self.container.attrs['Name']

    def get_status(self, ):
        return self.container.attrs['State']['Status']

    def get_port(self):
        return self.container.attrs['NetworkSettings']['Ports']['3000/tcp'][0]['HostPort']

    def __get_project_name(self):
        return  self.container.attrs['Config']['Labels']['com.docker.compose.project']

    def __get_service_name(self):
         return  self.container.attrs['Config']['Labels']['com.docker.compose.service']

    def get_ips(self):
        if len(self.container.attrs['NetworkSettings']['Networks'])>1:
            ip_address= get_master_ips(networks, self.container, self.__get_project_name())

        else:
            ip_address = self.container.attrs['NetworkSettings']['Networks'][self.__get_project_name()+'_'+self.__get_service_name()]['IPAddress']
        return ip_address


def map_master_ip_to_slave_ip(master_ips, slave_ip):

    slave_ip_parts = slave_ip.split(".")

    for x in range(len(master_ips)):
        if (slave_ip_parts[0] == master_ips[x].split(".")[0]
                and slave_ip_parts[1] == master_ips[x].split(".")[1]
                    and slave_ip_parts[2] == master_ips[x].split(".")[2]):
            return master_ips[x];

    return None


def get_master_ips (list_of_networks, container, project_name):
    """
    This gets all IPs for master
    """
    list_of_ips = []

    for network_name in list_of_networks:
        ip_address = container.attrs['NetworkSettings']['Networks'][project_name+'_'+network_name]['IPAddress']
        list_of_ips.append(ip_address)

    return list_of_ips

def is_process_running (log):
    """
    Determine if rails server/process is running
    """

    for line in log:
        if isinstance(line,str):
            if ('workspace' in line and 'puma' in line):
                print (line)
                return True

    return False

def verify_log_from_curl(log, container_requester, conainer_recepient=None):
    """
    Takes log returned after execution of CURL command inside of the Docker container
    """

    #VERIFY that <H1>Hello World<H1> is returned from curl
    for line in log:
        flag = False
        if isinstance(line,str):
            text = line
            if(len(text)>0):
                flag=True

            if (conainer_recepient is None):
                #VERIFY if connection was successful response is not empty
                print ("CURL from  " + str(container_requester) + " to self  is >>> " + str(flag) + '\n')

            else:
                #VERIFY if connection was successful response is not empty
                print ("CURL from  " + str(container_requester) + " to  " + str(conainer_recepient) + " is >>> " + str(flag) + '\n')

            if 'Hello World' in line:
                print ("CURL returned response with text <Hello World> "+'\n' )

    if (flag==False):
        print ("CURL from  " + str(container_requester) + " to  " + str(conainer_recepient) + " is >>> " + str(flag) + '\n')



def collect_active_caontainers_data(containers_list):
    """
    collect data form active containers that are running
    """
    counter=len(containers_list)

    for container in l:
        counter=counter-1;

        active_container = MyContainer(container);
        active_containers.append(active_container)

        #just to keep master container separate for testing
        if "master" in active_container.service_name:
            active_master.append(active_container)

        # printing out info for each active container
        print ('\n')
        print('Container ID>>> '+active_container.get_id()+'\n')
        print('Container Name>>> '+active_container.get_name()+'\n')
        print('Container Staus>>> '+active_container.get_status()+'\n')
        if "master" in active_container.service_name:
            print('Master IPs>>> ')
            print(', '.join(active_container.get_ips())+'\n')
        else:
            print('Container IP Address>>> '+active_container.get_ips()+'\n')

        if (counter>0):
            print ('=====================================')




print("========= COLLECTING DATA ABOUT RUNNING NODES =========")

collect_active_caontainers_data(l)

print("============= TEST 1 ==================\n")
print("========= CHECK IF PROCESS IS RUNNING FOR EACH INSTANCE =========\n")


for instance in active_containers:
    log = instance.container.exec_run('ps aux',
                        stderr=True,
                        stdout=True)

    #VERIFY that process is running
    print ("Is Rails process running for service " + str(instance.service_name)+" >>> "+str(is_process_running(log))+'\n')



print("============= TEST 2 ==================\n")
print("========= CLIENT CAN REACH APP =========\n")


# run curl inside of the container to see if Hello World is returned

for instance in active_containers:
    log = instance.container.exec_run('curl -s http://localhost:3000/ | grep "Hello world" && echo "OK" || echo "NOT"',
                     stderr=True,
                     stdout=True)

    verify_log_from_curl(log, instance.service_name)


print("============= TEST 3.1 ==================\n")
print("========= MASTER TALKS TO ALL NODES =========\n")

# run CURL from Master to every other node
for instance in active_containers:
    if not "master" in instance.service_name:
        log = active_master[0].container.exec_run('curl -s http://'+str(instance.get_ips())+':3000/',
                                                  stderr=True,
                                                  stdout=True)

        verify_log_from_curl(log,active_master[0].service_name, instance.service_name)


print("============= TEST 3.2 ==================\n")
print("========= ALL NODES TALK TO MASTER =========\n")


# run CURL from Master to every other node
master_ips = active_master[0].get_ips()
for instance in active_containers:
    if not "master" in instance.service_name:

        common_ip = map_master_ip_to_slave_ip(master_ips, instance.get_ips())
        log = instance.container.exec_run('curl -s http://'+common_ip+':3000/',
                                          stderr=True,
                                          stdout=True)

        verify_log_from_curl(log, instance.service_name, active_master[0].service_name)


print("============= TEST 3.3 ==================\n")
print("========= ALL NODES TALK OTHER NODES =========\n")

all_nodes_ips = []

#collecting all nodes ips to reach from other nodes
for i in range(len(active_containers)):
    if not "master" in active_containers[i].service_name:

        for k in range(i+1, len(active_containers)):
            if not "master" in active_containers[k].service_name:

                log = active_containers[i].container.exec_run('curl -s http://'+str(active_containers[k].get_ips())+':3000/',
                                          stderr=True,
                                          stdout=True,
                                          stream=True)

                verify_log_from_curl(log, active_containers[i].service_name, active_containers[k].service_name)




