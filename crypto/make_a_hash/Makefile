CC=gcc
C_FLAGS=-fno-stack-protector -no-pie -z execstack
              # disable canary: -fno-stack-protector
			  # disable PIE: -no-pie
C_LIBS= # -lcrypto or something

out=chal.py

.PHONY: all
all: $(out)

$(out): server.py
	cp $< $@
	chmod 755 $@

# container builds this target
# make sure 'all' builds everything you need
# container builds on ubu1804
.PHONY: container
container: all

.PHONY: clean
clean:
	$(RM) $(out) *.o
