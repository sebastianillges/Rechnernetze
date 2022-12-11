import base64
import socket

server = ("asmtp.htwg-konstanz.de", 587)
srcmail = "sebastian.illges@htwg-konstanz.de"
dstmail = "sebastian.illges@htwg-konstanz.de"
subject = "Test"
msg = "Message"

username = "rnetin"
password = "Ueben8fuer8RN"
usernameb64 = base64.b64encode(username.encode())
passwordb64 = base64.b64encode(password.encode())

mailContent = "From:<" + srcmail + ">\n" \
              "To:<" + dstmail + ">\n" \
              "Subject: " + subject + "\n" \
              + msg + "\n" \
              ".\r\n"



# Create socket and connect to server
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.settimeout(10)
socket.connect(server)
print("< " + server[0] + " " + str(server[1]))
recv = socket.recv(1024).decode()
print("> " + recv)

# HELO
# versteh ich nicht
'''
socket.send("HELO hä\r\n".encode())
print("< HELO hä")
recvHelo = socket.recv(1024).decode()
print("> " + recvHelo)
'''
# Login
socket.send("AUTH LOGIN\r\n".encode())
print("< AUTH LOGIN")
recvAuthLogin = socket.recv(1024).decode()
print("> " + recvAuthLogin)

# Username
socket.send(usernameb64 + "\r\n".encode())
print("< " + usernameb64.decode())
recvUsername = socket.recv(1024).decode()
print("> " + recvUsername)

# Password
socket.send(passwordb64 + "\r\n".encode())
print("< " + passwordb64.decode())
recvPassword = socket.recv(1024).decode()
print("> " + recvPassword)

# Mail from
socket.send(("MAIL FROM:<" + srcmail + ">\r\n").encode())
print("< MAIL FROM:<" + srcmail + ">")
recvFromMail = socket.recv(1024).decode()
print("> "+ recvFromMail)

# Mail to
socket.send(("RCPT TO:<" + dstmail + ">\r\n").encode())
print("< RCPT TO:<" + dstmail + ">")
recvToMail = socket.recv(1024).decode()
print("> "+ recvToMail)

# Data
socket.send(("DATA\r\n").encode())
print("< DATA")
recvData = socket.recv(1024).decode()
print("> " + recvData)

# Mail Content
socket.send(mailContent.encode())
print("< " + mailContent)
recvMail = socket.recv(1024).decode()
print("> " + recvMail)

# Quit
socket.send("QUIT\r\n".encode())
print("< QUIT")
recvQuit = socket.recv(1024).decode()
print("> " + recvQuit)

