import os
import subprocess

class SlurmScript:
    """
        Encapsulates a bash script to run on a server managed by slurm.
        Handles the writing and execution, of these scripts, and captures and stores
        any job numbers generated. This class also supports the import of modules,
        if this package is available on your system.
    """
    def __init__( self, command, script_name, slurm_args, dependency_mode = "afterany" ):
        """
            Constructor for SlurmScript class

            :param command: command to be run by slurm server, e.g., 'cat *.fasta'
             Note: bash shebang written to the file, but can be set by user if the standard
                  '#!/bin/bash' is not used by your system
             Note: srun will be prepended to the command, so the above becomes 'srun cat *.fasta'
             Note: multiple job steps can be included in a fasta file, but only one can be provided upon initialization
        
            :param script_name: name of the executable to be created by SlurmScript.write()

            :param slurm_args: list of slurm arguments to be written to the file. This
                               param is in the form of [ '--mem=4g', '--time=20:00', ... ]
             Note: the #SBATCH flag is written to the file before each of these arguments
        
            :param dependency_mode: Optional mode of dependencies this script is dependant upon.
        """
        self.commands = [ SlurmScript.Command( command ) ]

        self.slurm_args = list()
        for item in slurm_args:
            self.add_slurm_arg( item )
        
        self.script_name = os.getcwd() + '/' + script_name

        self.dependencies = list()
        self.dependency_mode = dependency_mode

        self.modules = list()
        self.job_num = 0

        self.sbatch = "#SBATCH "
        self.shebang = "#!/bin/bash "

    class Command:
        def __init__( self, string_command ):
            self.command = string_command
        def __str__( self ):
            return self.command
        def add_arg( self, to_add ):
            self.command += to_add

    def write( self ):
        """
            Writes the script, the name of the executable created is 
            determined by the class-member variable script_name
        
            Note: this method sets the mode to octal 755 r/w/x access
        """
        file = open( self.script_name, 'w' )

        file.write( self.shebang )
        file.write( "\n" )

        for item in self.slurm_args:
            if '--' in item[ 0 ]:
                file.write( self.sbatch + '='.join( item ) )
            else:
                file.write( self.sbatch + ' '.join( item ) )

            file.write( "\n" )

        if len( self.dependencies ) > 0:
            file.write( self.sbatch + "--dependency=" + self.dependency_mode + ':' + ','.join( self.dependencies ) )
            file.write( "\n" )


        for current_module in self.modules:
            file.write( "module load " + current_module )
            file.write( "\n" )

        for current_command in self.commands:
            file.write( "srun " + str( current_command ) )
            file.write( "\n" )

        file.close()

    def run( self ):
        """
            Executes the script, and returns the slurm job number

            Note: this method sets the mode access mode to octal 755 
        """
        os.chmod( self.script_name, 0o755 )
        script = subprocess.getoutput( "sbatch " + self.script_name ) 

        # Get and return the jobnumber
        script = script.split()[ 3 ]
        self.job_num = script

        return script

    def is_finished( self ):
        """
            Determines whether or not this job has been completed,
            where completion is determined by a job state code 
            that is neither PENDING nor RUNNING, not that this method does not
            determine the success/failure of any given job number, 
            only whether or not it is currently running.
        
            :returns: boolean True/False depending on whether or not a job is finished, or False
                      if the job has not started, and therefore has no job number
        """
        state_code = self.get_state_code()
        
        return ( state_code != None ) and ( !( state_code == 'PENDING' or state_code == 'RUNNING' ) )

    def get_state_code( self ):
        """
           Gets the state of a job, after it has been submitted to the slurm handler
           Note that because a job needs to have been started to have a job number,
           this method will return None if this job has no job number
            
           :returns: string state code of job, or None if 'self' has no job_number
        """
        job_state = None

        if self.job_num:
            job_state = subprocess.getoutput( "sacct -j %s -b -n -p -X " % self.job_num )
            job_state = job_state.split( '|' )[ 1 ]

        return job_state


    def set_shebang( self, new_shebang ):
        """
            Sets the shebang (Default '#!/bin/bash')
            to string new_shebang
        """
        self.shebang = new_shebang

    def add_command( self, in_command ):
        """
            Adds a command, (job-step) to be written to the output
            bash file.
        
            :param in_command: command to be written to the file, can be any
                               command recognized by your bash/slurm environment
            Note: srun is prepended to the command as it is written to the file, do not
                  include this yourself
        """
        self.commands.append( SlurmScript.Command( in_command ) )

    def add_slurm_arg( self, new_arg ):
        """
            Adds a new argument to be written to the executable created by this script,
        
            Note: before any slurm arguments are written to the file,
                  #SBATCH is written before any arguments, do not include it
                  here
            :param new_arg: argument to be written to script produced by this
                            obect's write method, in the format '--key=value', or 
                            of the form '-c 1'
        """
        if '--' in new_arg:
            self.slurm_args.append( new_arg.split() )
        else:
            self.slurm_args.append( new_arg.split( '=') )

    def add_dependencies( self, job_num_list ):
        """
            Add a list of dependencies that this object relies upon.
            
            :param job_num_list: list of job numbers this script is to rely upon
        """
        for current_job in job_num_list:
            self.dependencies.append( current_job )

    def add_dependency( self, job_num ):
        """
            Add a single dependency that this object depends on.
        
            :param job_num: job number for this script to rely on
        """

        self.dependencies.append( current_job )

    def set_dependency_mode( self, new_mode ):
        """
            Sets the dependency mode of this job's dependencies
            :param new_mode: slurm dependent mode of dependencies,
                             can include 'afterany', 'afterok', etc
        """
        self.dependency_mode = new_mode

    def add_modules( self, modules_list ):
        """
            Adds a list of string modules to be loaded before execution of
            any job steps in the script. 
        
            Note: 'module load ' is written to the file by the script, do not include this
                  before any of the dependencies in modules_list
            :param modules_list: list of string modules to load
                                 [ 'python/3.6', 'blast+', ... ]
        """
        for item in modules_list:
            self.modules.append( item )
        
    def add_module( self, to_add ):
        """
            Add a single string module to the list of modules 
            that will be loaded before execution of any jobsteps in script.

            Note: 'module load ' is written to the file by the script, do not include this
                  in to_add 
        
            :param to_add: string module to add
        """
        self.modules.append( to_add )

    def execute( self ):
        """
            Writes script according to its variables, 
            executes the script in a subshell,
            and then deletes the result once it has been started.

            :returns: string job_number of submitted sbatch job
        """
        self.write()
        job_number = self.run()
        os.remove( self.script_name )

        return job_number
 
