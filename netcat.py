import sys
import socket
import threading
import argparse
import subprocess

def parse_args():
	parser = argparse.ArgumentParser(description="Netcat Tool")

	parser.add_argument("-c", "--command", action=store_true, help="command shell")
	parser.add_argument("-t", "--target", default="0.0.0.0", help="specified IP")
	parser.add_argument("-p", "--port", type=int, default=5555, help="specified Port")
	parser.add_argument("-l", "--listen", action="store_true", help="listen")
	parser.add_argument("-e", "--execute", help="execute commands")
	parser.add_argument("-u", "--upload", help="upload a file")

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
				response = b""

				while b"<END>" not in response:
					data = self.socket.recv(4096)
					if not data:
						print("Connection closed by server.")
						self.socket.close()
						return
					response += data

				print(response.replace(b"<END>", b"").decode(), end="")

				buffer = input("") + "\n"

				if buffer.lower() in ["exit", "quit", "q"]:
					self.socket.send((buffer + "\n").encode())
					print("Closing connection...")
					self.socket.close()
					return

				self.socket.send((buffer + "\n").encode())

		except KeyboardInterrupt:
			print("\nUser terminates.")
			self.socket.close()
			sys.exit()

	def listen(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.socket.bind((self.args.target, self.args.port))
		self.socket.listen(5)

		print("[*] Server listening...")

		try:
			while True:
				client_socket, addr = self.socket.accept()
				print(f"[*]\n[*] Connection from {addr[0]}:{addr[1]}")

				client_thread = threading.Thread(
					target=self.handle,
					args=(client_socket,),
					daemon=True
				)
				client_thread.start()

		except KeyboardInterrupt:
			print("\n[!] Server shutting down...")


		finally:
			self.socket.close()
			print("[*] Socket closed cleanly.")

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
					data = client_socket.recv(64)

					if not data:
						return

					cmd_buffer += data

				cmd = cmd_buffer.decode().strip()

				if cmd.lower() in ["exit", "quit", "q"]:
					client_socket.send(b"Closing connection...\n")
					client_socket.close()
					return

				response = self.execute(cmd)

				if not response:
					response = b""

				client_socket.send(response + b"<END>")

if __name__ == "__main__":
	args = parse_args()
	nc = Netcat(args)

	if args.listen:
		nc.listen()
	else:
		nc.send()
