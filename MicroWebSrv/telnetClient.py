def telnets():
    import getpass
    import telnetlib

    HOST = "localhost"
    user = input("Enter your remote account: ")
    password = getpass.getpass()

    tn = telnetlib.Telnet(HOST)

    tn.read_until(b"login: ")
    tn.write(user.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

    tn.write(b"ls\n")
    tn.write(b"exit\n")

    print(tn.read_all().decode('ascii'))

    if __name__ == "__main__":
        telnets()

# not working good
# def subpross():
#     proc = subprocess.Popen('rshell --buffer-size=30 -p COM6 ; repl', 
#                         shell=True,
#                         stdin=subprocess.PIPE,
#                         stdout=subprocess.PIPE,
#                         stderr=subprocess.PIPE
#                         )
#     for i in range(10):
#         output = proc.stdout.readline()
#         print('out'+str(i)+': ', output.rstrip())
#     repl = 'repl'
#     proc.stdin.write(bytes(repl, encoding='utf8'))
#     for i in range(3):
#         output = proc.stdout.readline()
#         print('out'+str(i)+': ', output.rstrip())
    
#     # proc = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
#     # p2 = subprocess.Popen('print("res1")', stdin=proc.stdout, stdout=subprocess.PIPE)
#     # proc.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits
#     # out = p2.communicate()[0]
#     # out, err = proc.communicate(input=bytes("print('res1')", encoding='utf8'))
#     # print(out)
#     # print(err)

#     cmd = 'print("res1")'
#     p2 = subprocess.Popen(cmd, stdin = proc.stdout, stdout=subprocess.PIPE)
#     outs = p2.communicate()
#     # outs, errs = proc.communicate(timeout=15)
#     # output = proc.stdout.readline()
#     print('the result1 is', outs.rstrip())
#     cmd = 'print("res2")'
#     proc.stdin.write(bytes(cmd, encoding='utf8'))
#     output = proc.stdout.readline()
#     print('the result2 is', output.rstrip())