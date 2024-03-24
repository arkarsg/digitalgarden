# Linux kernel

- A major component of an OS
- Interface between computers hardware and its processes

**4 major tasks**
- Memory management
- Process management
- Device drivers
- System calls and security

`uname` : Kernel name

---
# Kernel space and user space

## Kernel
- Kernel
- Device driver

A process running in the kernel space has unrestricted access to the hardware

## User space
- Restricted access to memory and CPU

>[!example]
>An application in the userspace wishes to access data in the disk (hardware). It has to make requests to the kernel using syscalls
>

---

# Working with hardware
Device → Device driver → `uevent` → `udev` in the userspace → `/dev/sdb1`

CPU
- 32-bit : Predominant until the 1990s, register stores $2^{32}$ values
	- Must use 32-bit OS, software
- 64-bit
	- Can run both 32-bit and 64-bit CPU

$$
\text{total number of CPU (virtual)} = \text{number of cores and threads} \space \times \space \text{number of sockets}
$$
---

# Boot

1. BIOS POST
	- Power on Self Test – ensure that hardware connected to the device are configured correctly
2. Boot Loader (GRUB2)
	- Loads the boot code, first sector of the disk
	- Provides boot screen
	- Loads the kernel to mem
3. Kernel initialisation
	- Decompress the kernel
	- Loaded into the memory and start executing
	- Initialising hardware and mem management task
	- Runs an init task
4. Systemd (service initalisation)
	- Responsible for mounting file system


Find out the `systemd` used
`ls -l /sbin/init`

---

# Runlevels

- Graphical mode → `5`
- CLI mode → `3`

| **Run level** | **Systemd targets** | **Function**                      |
| ------------- | ------------------- | --------------------------------- |
| 5             | graphical.target    | Boots into graphical interface    |
| 3             | multiuser.target    | Boots into command line interface |

Find out the run level with

```sh
sudo systemctl get-default
```

Change run level with:
```sh
sudo systemctl set-default multi-user.target
```

---

# File types

> Every object in Linux can be considered a type of file

- Regular file
	- Images
	- Scripts
	- Config/ data files
- Directory
	- `/home/user`
- Special files
	- character files : Represents devices that allows the device to communicate with the OS
	- Block files : Represents the block devices (hard disks and RAMS)
	- Links
		- Symbolic : Pointer to another file
		- Hard link : Independent files but occupy the same data in block storage
	- Sockets : communication between two processes
	- Named pipes : Directional flow between 2 processes

`file` command displays the file type

---

# FS Hierarchy

- Third party programs → `/opt`
- Security software → `/mnt`
	- Mount file system temporarily in the file system
- `/tmp`
	- Store data temporarily in the file system
- `/media`
	- External media
- `/dev`
	- Contains special block and character device files
	- files for external devices
- `/bin`
	- Executalbes
- `/etc`
	- Config files
- `/lib`
	- shared libraries to be imported
- `/usr`
	- Location where all the data of userland resides
- `/var`
	- Logs and cached data

---