
Hardware has 2 modes
1. User mode
2. Kernel mode

**Kernel mode** has unrestricted access to hardware. I/O instructions and halt instructions are *privileged* and can only be executed in kernel mode.

==Process== is the fundamental unit of work in OS
- Process management
	- Creation and deletion
	- Mechanisms for processes to communicate and synchronise

---

# OS structures

![os-structure|800](Pasted%20image%2020240316000349.png)

==User interface== 
- Command Line Interface, batch interface, graphical user interface
- direct I/O, keyboard to enter text etc

==Program Execution==
- Load a program into memory and run that program
- Program must be able to end its execution, either *normally* or *abnormally*

==I/O Operations== 
- May require IO which may involve a file or a device
- **User space cannot control I/O devices directly** 
- Therefore, the OS must provide a means to do IO.

==File System Manipulation==
- In Linux, everything is a file
- Read/ Write. Delete, Search, List file information, permissions

==Communications==
- Exchange information with another process
- Can be between processes on the same computer or different computer systems tied together by a computer network.
- May be implemented by shared memory

==Error detection==
- mem error, seg fault, connection failure, no paper, arithmetic overflow, runtime error.
- For each type of error, the OS needs to take appropriate action or halt the system, terminate the process or return an error code

==Resource Allocation== 
- multiple users or multiple jobs → manage CPU cycles, main mem, file storage

---

# System calls

APIs between processes and OS. Processes in the *user space* have no access to the resources → call services in the kernel.

- Requires change from *user mode* to *kernel mode*

>[!example]
>- User program invokes the library call
>    - Using the normal function call mechanism in stack
>- Library call places the system call number in a designated location
>    - register
>- Library call executes a special instruction to switch from user mode to kernel mode
>    - This is commonly known as **TRAP (as in trapdoor)**
>- In kernel mode, determine the appropriate system call handler. This is handled by dispatcher using system call number as index
>- System call handler is executed and carries out the actual request
>- System call handler ended and returns control to library call
>    - Switch from kernel mode to user mode
>- Library call return to the user program via function return.