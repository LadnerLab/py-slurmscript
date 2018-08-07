**SlurmScript( script_name, command, slurm_ages, dependency_mode = "afterany" )**
```
Constructor for SlurmScript class

:param command: command to be run by slurm server, e.g., 'cat *.fasta'
Note: bash shebang written to the file, but can be set by user if the standard
'#!/bin/sh' is not used by your system
Note: srun will be prepended to the command, so the above becomes 'srun cat *.fasta'
Note: multiple job steps can be included in a fasta file, but only one can be provided upon initialization

:param script_name: name of the executable to be created by SlurmScript.write()

:param slurm_args: list of slurm arguments to be written to the file. This
param is in the form of [ '--mem=4g', '--time=20:00', ... ]
Note: the #SBATCH flag is written to the file before each of these arguments

:param dependency_mode: Optional mode of dependencies this script is dependant upon.
```
**SlurmScript.write()**
```
Writes the script, the name of the executable created is 
determined by the class-member variable script_name

Note: this method sets the mode to octal 755 r/w/x access
```
**SlurmScript.run()**
```
Executes the script, and returns the slurm job number

Note: this method sets the mode access mode to octal 755 
```
**SlurmScript.is_finished()**
```
Determines whether or not this job has been completed,
where completion is determined by a job state code 
that is neither PENDING nor RUNNING, not that this method does not
determine the success/failure of any given job number, 
only whether or not it is currently running.

:returns: boolean True/False depending on whether or not a job is finished, or False
          if the job has not started, and therefore has no job number

```
**SlurmScript.get_state_code**
```
Gets the state of a job, after it has been submitted to the slurm handler
Note that because a job needs to have been started to have a job number,
this method will return None if this job has no job number
            
:returns: string state code of job, or None if 'self' has no job_number
```
**SlurmScript.set_shebang( new_shebang )**
```
Sets the shebang (Default '#!/bin/bash')
to string new_shebang
```
**SlurmScript.add_command( in_command )**

```
Adds a command, (job-step) to be written to the output
bash file.

:param in_command: command to be written to the file, can be any
command recognized by your bash/slurm environment
Note: srun is prepended to the command as it is written to the file, do not
include this yourself
```
**SlurmScript.add_slurm_arg( new_arg )**
```
Adds a new argument to be written to the executable created by this script,

Note: before any slurm arguments are written to the file,
#SBATCH is written before any arguments, do not include it
here
:param new_arg: argument to be written to script produced by this
obect's write method, in the format '--key=value', or 
of the form '-c 1'
```
**SlurmScript.add_dependencies( job_num_list )**
```     
Add a list of dependencies that this object relies upon.

:param job_num_list: list of job numbers this script is to rely upon
```
**SlurmScript.add_dependency( job_num )**
```     
Add a single dependency that this object depends on.

:param job_num: job number for this script to rely on
```
**SlurmScript.set_dependency_mode( new_mode )**
```     
Sets the dependency mode of this job's dependencies
:param new_mode: slurm dependent mode of dependencies,
		can include 'afterany', 'afterok', etc
```
**SlurmScript.add_modules( modules_list )**
``` 
Adds a list of string modules to be loaded before execution of
any job steps in the script. 

Note: 'module load ' is written to the file by the script, do not include this
before any of the dependencies in modules_list
:param modules_list: list of string modules to load
[ 'python/3.6', 'blast+', ... ]
```
**SlurmScript.add_module( to_add )**
```     
Add a single string module to the list of modules 
that will be loaded before execution of any jobsteps in script.

Note: 'module load ' is written to the file by the script, do not include this
in to_add 
:param to_add: string module to add
```
**SlurmScript.execute()**
``` 
Writes script according to its variables, 
executes the script in a subshell,
and then deletes the result once it has been started.

:returns: string job_number of submitted sbatch job
```

