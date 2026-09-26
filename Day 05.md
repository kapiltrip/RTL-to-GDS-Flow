# Day 05 — Tutorial 1 — Unix foundations for EDA

[Course index](README.md) · Week 1 · [Lecture video](https://www.youtube.com/watch?v=ztPFMRfpPfk) · [Handwritten index](Handwritten%20Index.md)

## Outline

- [A shell is the working interface](#a-shell-is-the-working-interface)
- [Navigation and file operations](#navigation-and-file-operations)
- [Help, permissions, disk space, and processes](#help-permissions-disk-space-and-processes)
- [Foreground and background jobs](#foreground-and-background-jobs)

## A shell is the working interface

![The tutorial demonstrates file and directory commands in a Linux shell](images/Day%2005/01-unix.png)

*Video frame: [4:18](https://www.youtube.com/watch?v=ztPFMRfpPfk&t=258s). The tutorial demonstrates file and directory commands in a Linux shell*


This tutorial is presented by **Jasmine Kaur**, the course teaching assistant. It introduces Unix-style command-line work used to launch tools, manage design files, inspect logs, and control long-running jobs. A **shell** interprets commands; a **terminal** provides the text interface through which you interact with it. The **working directory** is the directory against which relative paths are resolved.

On Windows, WSL provides a Linux environment. The tutorial demonstrates `wsl --install` from administrator PowerShell, a restart, and initial Linux-user setup. The exact installation path depends on the existing Windows/WSL state; [Microsoft's current installation instructions](https://learn.microsoft.com/en-us/windows/wsl/install) describe the prerequisites and supported command. This chapter documents the lesson; no WSL installation was performed for these notes.

There is no dedicated Unix page in the uploaded handwriting. The Tcl note belongs to [Day 10](Day%2010.md), because a Tcl interpreter and a Unix shell are different command environments.

## Navigation and file operations

| Command | Meaning | Detail that prevents a common mistake |
|---|---|---|
| `pwd` | Print working directory | Check it before interpreting a relative path |
| `ls` | List directory entries | `ls -a` also includes hidden names beginning with `.` |
| `cd path` | Change working directory | `cd ..` goes to the parent; `cd` normally goes home |
| `mkdir tutorial1` | Create a directory | The directory name is an argument, not a command |
| `mv a.txt tutorial1/` | Move a file | The original pathname no longer refers to it after success |
| `cp a.txt a_copy.txt` | Copy a file | The source remains; an existing destination can be overwritten |
| `touch d.txt` | Update timestamps, creating a file if absent | It does not erase an existing file's contents |
| `rm d.txt` | Remove a file | Ordinary shell removal does not provide a desktop recycle-bin workflow |
| `cat a.txt` | Write file contents to standard output | Best suited to text; large logs are easier to page or search |

An **absolute path** starts from the filesystem root, such as `/home/student/lab`; a **relative path** is interpreted from the current directory, such as `rtl/top.v`. Quote paths containing spaces. Linux filenames are generally case-sensitive: `Top.v` and `top.v` can name different files.

This small practice sequence creates a fresh directory and copies a file without deleting any study material:

```bash
mkdir tutorial1_practice
cd tutorial1_practice
pwd
touch example.txt
cp example.txt example_copy.txt
ls
```

Expected result: both filenames appear in the new directory. `touch` creates an empty file here because the name did not exist. Running the sequence again requires accounting for the already-created directory; shell commands change persistent filesystem state.

## Help, permissions, disk space, and processes

| Command | What it answers |
|---|---|
| `which cat` | Which executable is found through the search path, for this external command? |
| `man ls` | What does the local manual say about `ls` and its options? |
| `sudo command` | Run an authorized command with elevated or another user's privileges |
| `du -h directory` | How much allocated disk space do these directory contents use? |
| `df -h` | How much space is used and available on mounted filesystems? |
| `ps` | What processes are selected by this invocation and its options? |
| `top` | How are processes and system resources changing over time? |
| `history` | What commands are recorded by the shell's history feature? |
| `whoami` | What is the current effective username? |

`du` and `df` answer different questions and need not show the same number. A small `du` result for one project does not prove the filesystem has free space. Plain `ps` usually selects only a subset of processes; “all processes” requires appropriate options such as `ps -e` on common Linux systems.

In the tutorial, `sudo apt-get update` refreshes package metadata. It does not by itself upgrade every installed package. `sudo` is a privilege boundary, not a prefix to add automatically whenever an ordinary command fails. Shell built-ins such as `cd` also differ from external executables; `type cd` can identify a built-in where `which` is less informative.

## Foreground and background jobs

The tutorial runs `sleep 100`, suspends it with Ctrl+Z, resumes it with `bg %1`, and returns it to the foreground with `fg %1`. `sleep` delays that process; it does not put the whole computer into sleep mode.

**A process ID (PID)** identifies an operating-system process. **A job number** such as `%1` identifies a job tracked by the current shell. They are not the same identifier. Ctrl+Z ordinarily suspends a foreground job; `bg` resumes a stopped job in the background; `fg` brings a job into the foreground. `jobs` lists the shell's jobs. A trailing `&` starts a command asynchronously. These distinctions are described in the [GNU Bash manual](https://www.gnu.org/software/bash/manual/bash.html#Job-Control).

For EDA, this matters when a simulation or implementation run takes a long time. A background process still consumes resources and can still write to files. Backgrounding is not the same as making a job survive logout or a terminal shutdown.

**Recall checks:** Why does `cd` have to affect the shell itself? What is the difference between `%1` and PID 1? Why can a failed `cp` command result from a wrong working directory rather than missing privileges?

[Previous: Day 04](Day%2004.md) · [Next: Day 06](Day%2006.md)
