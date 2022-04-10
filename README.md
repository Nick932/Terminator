# Terminator
Terminator is a script, which is looking for files meets
the pointed criteria. Terminator will find and show
such files to you. If you will agree, the script will delete them.

# Usage
Correct format of calling this script using shell:
python3 terminator.py <criteria> <value> <comparing_type> <root_directory_to_process>

· criteria - the attribute of file which we are using to decide if it will be deleted or not.
  Available criteria for now:
        - file_extension(expected value: string without dots)
        - file_size(expected value: size in bytes)

· value - the value of criteria. For example: txt

· comparing_type - the way to compare values. Available comparing types:
        - equal
        - lower
        - bigger

· root_directory_to_process - optional argument, must be a full path (no slash at the end). 
  By default - current directory of script.

# Contacts

Telegram: @MaikSturm932
