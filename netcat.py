import sys
import socket
import threading
import argparse
import subprocess

def parse_args():
	parser = argparse.ArgumentParser(description="Netcat Tool")

	parser.add_argument("-t", "--target", default="0.0.0.0")
	parser.add_argument("-p", "--port", type=int, default=5555)
	parser.add_argument("-l", "--listen", action="store_true")
	parser.add_argument("-e", "--execute")
	parser.add_argument("-u", "--upload")

	return parser.parse_args()

class Netcat:
	def __init__(self, args):
		self.args = args
		self.buffer = b""

	def send(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.args.target, self.args.port))

		try:
			if self.buffer:
				self.socket.send(self.buffer)

			while True:
				response = self.socket.recv(4096)
				if not response:
					return

					response += data

				print(response.decode(), end="")

				buffer = input("") + "\n"

				self.socket.send((buffer + "\n").encode())

		except KeyboardInterrupt:
			print("\nUser terminates.")
			self.socket.close()
			sys.exit()

	def listen(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((self.args.target, self.args.port))
		self.socket.listen(5)

		while True:
			client_socket, addr = self.socket.accept()
			print(f"[*]\n[*] Connection from {addr[0]}:{addr[1]}")

			client_thread = threading.Thread(
				target=self.handle,
				args=(client_socket,)
			)
			client_thread.start()

	def execute(self, cmd):
		cmd = cmd.strip()
		if not cmd:
			return b""

		try:
			output = subprocess.check_output(
				cmd,
				stderr=subprocess.STDOUT,
				shell=True
			)
		except subprocess.CalledProcessError as e:
			output = e.output or b"Command failed\n"

		return output

	def handle(self, client_socket):
		if self.args.execute:
			output = self.execute(self.args.execute)
			client_socket.send(output)

		elif self.args.upload:
			file_buffer = b""

			while True:
				data = client_socket.recv(4096)

				if not data:
					break
				file_buffer += data

			with open(self.args.upload, "wb") as f:
				f.write(file_buffer)

			client_socket.send(b"File saved")

		else:
			while True:
				client_socket.send(b"<BHP: #> <END>")
				cmd_buffer = b""

				while b"\n" not in cmd_buffer:
					cmd_buffer += client_socket.recv(64)

				cmd = cmd_buffer.decode().strip()

				if cmd.lower() in ["exit", "quit", "q"]:
					client_socket.send(b"Closing connection...\n")
					client_socket.close()
					break

				response = self.execute(cmd)
				client_socket.send(response)

if __name__ == "__main__":
	args = parse_args()
	nc = Netcat(args)

	if args.listen:
		nc.listen()
	else:
		nc.send()
