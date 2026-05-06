# Networking and Exploitation Lab

This repository documents my hands-on learning journey while studying networking and basic offensive security concepts using Python.

Instead of just reading theory, I implemented everything step-by-step and tried to understand how client-server communication actually works at a low level.

---

## 📌 What this project contains

- TCP client implementation (`tcp_client.py`)
- TCP server implementation (`tcp_server.py`)
- UDP client implementation (`udp_client.py`)
- A custom Netcat-like tool (`netcat.py`)

---

## 🧠 What I learned

While building these tools, I understood:

- How TCP connections are established and managed
- Difference between TCP and UDP communication
- How sockets send and receive data internally
- Why TCP does not preserve message boundaries
- How real tools like Netcat work under the hood
- How command execution works using subprocess

---

## ⚠️ Problems I faced (and solved)

This part took most of the time — I faced multiple issues:

- Commands repeating due to buffer not resetting (`cmd_buffer` bug)
- Mixed and duplicated outputs due to improper `recv()` handling
- Client hanging because there was no clear end-of-response signal
- Designed a custom protocol using `<END>` to fix TCP stream issues
- Got `ConnectionResetError` when client closed before server response
- Handling partial data in `recv()`
- Interactive commands like `cat` blocking execution
- Difference between behavior of my Python client vs `nc`

---

## ⚙️ Example usage

### Start server
```bash
python netcat.py -t 0.0.0.0 -p 5555 -l -c
```

### Connect as client
```bash
python netcat.py -t 127.0.0.1 -p 5555
```

### Execute a command
```bash
python netcat.py -t 0.0.0.0 -p 5555 -l -e="cat /etc/passwd"
```

---

## 📌 Note

This is not a production-ready tool.
It is a learning project that reflects my debugging, mistakes, and understandings.
