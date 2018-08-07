# Py-SlurmScript
Python wrapper for batch scripts to be executed on a slurm-based HPC cluster. Provides support for modules, dependencies, multiple job-steps, 
and any number of slurm arguments.

### API
API Documentation can be found [here](docs.md)

### Example

``` python
import slurm_script

script = slurm_script.SlurmScript( "echo $(PWD)", "test_script", 
                                   [ '--time=20:00', '-c 1', '--mem=4G' ], 
								   dependency_mode = "afterok" 
								 )

script.add_modules( [ 'python/3.latest', 'blast+' ] )
script.add_module( 'usearch' )

script.write()
job_number = script.run()

```
The resulting script looks like 
``` bash
#!/bin/sh 
#SBATCH --time=20:00
#SBATCH -c 1
#SBATCH --mem=4G
module load python/3.latest
module load blast+
module load usearch
srun echo $(PWD)
```

