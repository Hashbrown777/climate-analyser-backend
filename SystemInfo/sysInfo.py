import psutil

def getInfo():
        #print("Process list: ")
        #print psutil.get_process_list() 
        print "cpu usage: "
        print psutil.cpu_percent(1)
        print "Memory Usage: "
        print psutil.virtual_memory()
        print "Disk Usage: "
        print psutil.disk_usage('/')
        print "Network info: "
        print psutil.network_io_counters(True)


def main():
        getInfo()

if __name__ == '__main__':
        exitCode = main()
        exit(exitCode)

