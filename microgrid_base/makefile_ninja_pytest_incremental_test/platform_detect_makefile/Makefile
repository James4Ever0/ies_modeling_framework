PLATFORM := $(shell python -c "import os; print(os.name)")
ifeq (${PLATFORM}, )
PLATFORM := $(shell python3 -c "import os; print(os.name)") # executed on macos
endif

# macos: posix.
main:
	echo ${PLATFORM}