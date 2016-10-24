#/bin/bash

#cat $1|while read line;do curl -x $line www.baidu.com -m 5 -connect-timeout 5 -o /dev/null -s -w "$line "%{http_code}"\n";done > $2 #| awk '{if($2==000)print $1}' > $2

cat ip.txt
