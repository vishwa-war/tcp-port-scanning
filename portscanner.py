# Importing socket library for establishes bidirectional communication channels between different devices over a network
import socket
import threading
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor

def scann(target, port):

	if port == 1:
		# Create a pool of 100 worker threads to scan multiple ports concurrently,
		# Significantly reducing scan time compared to sequential scanning.
		with ThreadPoolExecutor(max_workers=100) as executor:

			for port in range(1, 65536):
				executor.submit(scanall, ip, port)
	else:
		# Create a TCP socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Setting Socket time out for 1 second after it will exit from the loop
		sock.settimeout(1)

		# Attempt a TCP connection to the target port
		res = sock.connect_ex((ip,port))


		# Result code 0 indicates the port accepted the connection
		if res == 0:
			try:
				# Banner Grabbing to get the service version of the ports
				banner = sock.recv(1024)
				banner_decode = banner.decode(errors="ignore").strip()
				if banner_decode:
					print("port ",port," is open and the version is ",banner_decode)
				else:
					print("port ",port,"is open")
			except:
				print("port ",port,"is open")
		else:
			print("port ",port," is close")

		sock.close()

def scanall(target, port):

	# Create a TCP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Setting Socket time out for 1 second after it will exit from the loop
	sock.settimeout(1)

	# Attempt a TCP connection to the target port
	res = sock.connect_ex((ip,port))
	
	if res == 0:
		try:
			# Banner Grabbing to get the service version of the ports
			banner = sock.recv(1024)
			banner_decode = banner.decode(errors="ignore").strip()

			if banner_decode:
				print("port ",port," is open and the version is ",banner_decode)
			else:
				print("port ",port,"is open")
		except:
			print("port ",port,"is open")
	
	sock.close()

# Target can be a URL or a IP address to scan the ports
target = input("Enter Target URL or IP address: ")

# Giving an input port number to scan that port and say if it is open or close. 
port = int(input("Enter Port Number or 1 for aggresive scan: "))

# Getting IP address using host name
try:
	ip = socket.gethostbyname(target)
except socket.gaierror:
	print("Invalid Hostname")
	exit()

# Creating a Thread
t1 = threading.Thread(target=scann, args=(ip, port))

# Trying to Ping to the target IP address to get the ttl value based on that we can guess the OS
result = subprocess.run(["ping", "-4", "-n", "1", ip], capture_output=True, text=True)

output = result.stdout

match = re.search(r"TTL=(\d+)", output, re.IGNORECASE)

if match:
    ttl = int(match.group(1))
else:
    print("TTL not found")
if ttl > 64 and ttl < 128:
	print("The Running Operating System is Likely Windows")
else:
	print("The Running Operating System is Likely Linux")
	
t1.start()
t1.join()