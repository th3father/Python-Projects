# Python-Projects

I started to write my own tools in pyhton. Here, I describe more about these projects.
<br><br>

### BruteForce
Set of bruteforcers for different services, including SSH. Options:
  - Accepts custom timeout amount to create bruteforce strategy.
  - Accepts file input for usernames/passwords.
  - Accepts custom port.

### IpInfo
A tool for getting basic info about domains and ips, including:
  - Ip owner
  - Geolocation
  - Timezone
 
### Scanner
Ip/Port scanner.
  - Accepts ip range and CIDR.
  - Uses nmap top1000 and top20 ports, also it accepts ranges of IPs.
  - Accepts custom timeout amount for creating scan strategy.
 
 ### Searcher
 A strong tool for searching directories for sensitive files/data. Options:
  - Can search recursively.
  - Accepts custom list of file names to search for.
  - Accepts custom list of strings to search for in the files.
  - Accepts custom list of extension for files to search in/for.
  
 ### WebHeaderChecker
 Requests the headers from target websites and checks for the availability of interesting headers, like:
  *Strict-Transport-Security*
  *Content-Security-Policy*
  *X-Frame-Options*
  *Server*
