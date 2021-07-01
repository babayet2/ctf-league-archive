# OSUSEC 2020-2021 CTF LEAGUE ARCHIVE
The [OSUSEC](https://www.osusec.org/) 
CTF League is a remote internal CTF 
competition created to facilitiate learning
during the COVID-19 pandemic.
Challenges were released throughout the year,
and teams were guided towards the solutions
by a set of coaches on discord.
This archive contains the challenges written
for the inagural year.

## Challenges
NAME | CATEGORY | DESCRIPTION | POINTS 
-|-|-|-
rsa1 | crypto | a public key crypto intro challenge | 200 
make-a-hash | crypto | generate a collision for an insecure hash scheme | 300
nonsense | crypto | exploit nonce misuse | 300
rsa2 | crypto | who needs padding? | 300
secure-voting | crypto | find the MPC voting vuln to prevent a hostile takeover of OSUSEC | 300
copper | crypto | launch a coppersmith attack | 400
super-secure-voting | crypto | find the MPC voting vuln to prevent a hostile takeover of OSUSEC, but harder | 600
snowcone | malware | an introductory malware challenge | 250
LogCabin | malware | realistic incident response | 600
rayhanns-return | misc | track down an evildoer with open-source intelligence | 200
russian-nesting-bathhouse | misc | steeeeeegoooo |200
scrambled-noodles | misc | steeeeeeeeeeeegooooooooo | 200
many-time-pad | misc | a challenge to help our users set up their linux environments | 250
boxy | misc | linux misconfiguration scavenger hunt | 300
NCEP-XQC | pwn | easy pwn, no binary exploitation knowledge required | 100
pwn-review | pwn | a review of pwn concepts | 150
mash | pwn | buffer overflow |200
NCEP-BOTEZ | pwn | buffer overflow in a wrapper program | 200
printf-is-echo | pwn | format string vulnerability | 200
ret2win | pwn | control flow hijacking intro | 300
cookie | pwn | bad stack cookies | 350
unprintable | pwn | an exercise in shellcoding | 350
NCEP-MAGNUS | pwn | exploit a use-after-free in a simple process scheduler | 600
web1 | web | SQL injection and command injection | 200
web2 | web | blind SQL injection | 300
web3 | web | server-side template injection | 300
almostnopship0 | web | escape a python web sandbox | 350
web4 | web | server-side request foregery | 400

### Running Challenges
The challenges that required remote infrastructure
can be run locally with [docker](https://docs.docker.com/get-started/).

To build and run a challenge, 
simply enter its directory and run
the following two lines:
```bash
docker build . -t CHALLENGE_NAME
docker run -p PORT:PORT -d CHALLENGE_NAME
```

where CHALLENGE\_NAME may be set arbitraily, and
PORT is defined in the Dockerfile.

### Solutions
Solutions may be found in the `tests` directory
for each challenge.

## Results
After a fierce competition,
the following OSU students took the top
three spots in the CTF League scoreboard

1. [Cameron McCawley](https://cameron-mccawley.github.io/)
2. [Allen Benjamin](https://github.com/BobbySinclusto)
3. Kai Phan

## Authors & Coaches
* [Aaron Esau](https://aaronesau.com/)
* Aaron Jobe
* [Ryan Kennedy](https://github.com/TheREK3R)
* [Stan Lyakhov](https://github.com/Athos213)
* [Andrew Quach](https://github.com/Aqcurate)
* [Hadi Rahal-Arabi](https://github.com/babayet2)
* [Lyell Read](https://github.com/lyellread)
* [Lance Roy](https://ldr709.gitlab.io/)
* [Zander Work](https://zanderwork.com/)
