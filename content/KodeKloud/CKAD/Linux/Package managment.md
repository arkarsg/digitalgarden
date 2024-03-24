>[!note]
>Different Linux distributions uses different package managers

CentOS is forked from RHEL which is a paid-only enterprise distribution

**Software package**
- Contains all the software binaries and data

Different distributions runs different sets of tools and libraries, sometimes even different kernels.

Packages include a list of dependencies to run the packaged software on a given computer.

A package manager is a software in the Linux OS
- Package integrity and authenticity
- Simplified package management – to update, install software
- Grouping packages
- Manage dependencies – prevent dependency hell

## Types of Package managers
- `dpkg` - Package manager for debian
- `apt` - Newer frontend for `dpkg`
- `apt-get` - the default frontend for `dpkg`
- `rpm` – For RHEL based distro
- `yum` – frontend for `rpm`
- `dnf` – more feature rich frontend for `rpm`

---

# `RPM`

- File extension `.rpm`

Modes of operation:
- Installation
- Uninstalling
- Upgrade
- Query
- Verifying

```bash
rpm -ivh telnet.rpm
```

# `YUM`
High level package manager – automatic dependency resolution