Linux is the main OS for container orchestration

# Shell
**Home directory**
`/home/username`
- A home directory is unique for the user
- Read, write, delete access to the files in that directory if you are `user`
- `~` is used to represent the home directory

---
## Command Line Arguments

`<command> <option> <args>`

**Types**
- Internal (built-in) commands
	- Part of the shell itself and comes bundled with it
- External commands
	- Binary programs or scripts
	- Maybe preinstalled with a binary package manager

`type <command>` → find out if the command is internal or external

`mkdir -p parent/sub` → Creates both the parent and sub directory

---

## Directories

`cd` can use abs path or rel path.

**abs path**
`cd /home/user/folder`

**rel path**
`cd folder`

`pushd` and `popd`
- Treat routes like a stack

---

## Files

Output contents of the file:
```sh
cat /home/user/folder/file.txt
```

**Pagers**

```sh
more file.txt
```

Loads the file page at a time

---

# Shell types

- Bourne shell `sh`
- C shell `csh`
- Korn shell `ksh`
- Z shell `zsh`
- Bourne again shell `bash`
