# Boxy

## Description:

Time to poke at a linux box and see what there is to find. Im going to give you the flag right now, and the program to decrypt it too! 

You will have to find 7 flags to solve this challenge! They will be combined through Shamir Secret Sharing, and allow you to decrypt the flag!

The shares will go into shares.csv like this

```
x1,y1
x2,y2
```

and so on.

You will need python3-pip to install the decrypt dependencies. Nmap to be nmap, netcat to be netcat, and john the ripper, to do some light password cracking.

GLHF!


## How to solve

### Part 1

`nmap` to find 2 open ports 1337 and 13337

`nc` to 1337 gives you a nice long b64 string which will change every time you query the host.

`b64 -d` gives you a mess, but will always have a repeating pattern at the front. This should lead the player to suspect basic 1 byte xor. Its easy to xor the first part of the string with all 256 chars and pick the correct one from there to decode the rest of the string.

The output is "nonsense:username:b64string:flag"

The b64 string decodes into an `ssh` key for the aforementioned user

### Part 2

`ssh` using the key recovered above, to the user frederick, on port 13337.

Fred will have a top 100 passwords list and a password guide in their home dir. They will also have read access to /etc/shadow.bak

In here is a second flag and a hash for a user called oldadmin

Using john they will need to add the rule `Az"[0-9][0-9]"` or find another way to augment the wordlist and crack the hash.

The password is `freedom42`.

### Part 3

/etc/sudoers is world readable, and oldadmin can use sudo to run a script /root/script/adopt_dog

This creates a user named dog, with a home directory at /home/dog

create a user with `sudo /root/script/adopt_dog -p \`openssl passwd -6 lol\`` and log into dog with password lol. There will be a flag in dog's home dir

### Part 4

Why is there a flag in dog's home dir? Its because of /etc/skel, which is one of the open parameters in the adopt_dog script. Use the --skel option to select `--skel /root/.ssh` This will make the /home/dog directory contain root's private ssh key and another flag.

### Part 5

Root has their own ssh key in their authorized keys so ssh to be root now. There is another flag in the root .bashrc file

### Part 6

Root has access to `/opt/what/this/is/interesting/follow/this/path/to/get/a/flag/where/does/it/end/wow/this/is/taking/a/while/hmm/okay/tap/tap/tap/tap/tap/tap/hmm/here/you/go/lol/flag`, for a flag.

### Part 7

There is a running service on port 1338 that can only be reached from localhost `nc localhost 1338` to get the last flag.

### Finally

Place all flags in shares.csv in the same directory as flag.enc. Run my python script and get out the flag.

Woop.
