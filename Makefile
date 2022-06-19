.DEFAULT_GOAL := copy

SRC_PATH = ./apex/src

files = $(wildcard $(SRC_PATH)/*.py)

check: $(files)
	@mypy $(SRC_PATH)/

copy: $(files)
	@echo $? | xargs -n 1 echo | xargs -I{} cp ./{} /mnt/apex
	@touch $@

clean: FORCE
	rm copy

mount: FORCE
	sudo mount /dev/sda1 /mnt/apex

monitor: FORCE
	minicom -b 115200 -o -D /dev/ttyACM0

unmount: FORCE
	sudo umount /mnt/apex

FORCE: ;