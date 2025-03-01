Linux and shell scripting 
OS: is between your software and hardware 
Linux is the best because it’s Free, Open source, secure, many distributions, fast 

Fundamental of shell scripting 
Shell is the way you talk to your OS using command line (it’s what we call shell commands)

Manual  automate 

To write shell scripting you need a file like first-shell-scritp.sh 
Ls , ls -ltr, man , touch , mkdir , top , df -h , nproc, 
Ps, ps -ef | grep “amazon” 
. Linux and shell scripting 
OS: is between your software and hardware 
Linux is the best because it’s Free, Open source, secure, many distributions, fast 

Fundamental of shell scripting 
Shell is the way you talk to your OS using command line (it’s what we call shell commands)

Manual  automate 

To write shell scripting you need a file like first-shell-scritp.sh 
Ls , ls -ltr, man , touch , mkdir , top , df -h , nproc,  free -g 
#!/bin/sh/ name shebang (bash, dash, sh, ksh)
Test.sh | grep 1
| pipe command send the output of the fist command to the second command 
Set -x  # debug mode
Set -e   # exit the script when there is an error
Set -o pipefail
Set -exo pipefail 
Data | echo “data is “ 
Stdin stdout stderr 

Ps -ef | grep amazon “ awk -F” “ ‘{print $2}
#!/bin/sh/ name shebang (bash, dash, sh, ksh)

Find error in the logfile 

Curl command get information from internet | grep ERROR
Curl -X GET api.foo.com

Wget download the file instead whereas curl get information directly 

Find command 
Find / -name  
Sudo su – 

If and else in shell 
If [expression]
Then 
	Do this 
Else 
	Do this 
Fi 

A=4
B=10 
If [$a > $b]
Then 
	Echo “a is gret then b”
Else 
	Echo “bi is greater the n  b
Fi 

For I in [1.100}; do echo $1; done 

Trap command for trap signal 
Kill -9 id 
Linux signal : 

Trap “echo don’t use the ctrl+c” SIGINT 
Trap ‘rm -rf *’ SIGINT




