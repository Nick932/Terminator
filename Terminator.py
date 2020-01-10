'''''''''
In this scrpit you can choose directory for seeking and
the lowest avalible size. Files with lower size will be deleted.

You can use it by shell: "python3 Terminator.py tree_path minimal_size"

Created by Nickel.

'''''''''


import os,  sys


def asking(lis):
    print('Next files was founded:')
    for each in lis:
        print('\n'+str(each))
    while True:
        answer = input('Would you like to terminate this files? Input "Y" for yes, and "N" for "no"-answer.')
        if answer == 'Y':
            return True
        if answer == 'N':
            return False
        else:
            print ('Incorrect answer. Please, try again.')

def terminator(tree, minimal_size):
    termination_list = []
    for (thisdir,  subdirs,  fileshere) in os.walk(tree):
        for each in fileshere:
            if str(each)!= 'Terminator.py':
                # Lets see size of file...
                fullFilePath = str(thisdir)+str(os.sep)+str(each)
                stats = os.stat(fullFilePath)
                if stats.st_size<minimal_size:
                    termination_list.append(fullFilePath)
    if asking(termination_list) == True:
        try:
            os.remove(fullFilePath)
        except Exception:
            print('WARNING!\nSome unknown error was occured:',  sys.exc_info())
        except PermissionError:  
            print('WARNING!\nTermination of file', fullFilePath, 'is not permitted. File skipped.')
        else:
            print('File', str(each), 'from directory', thisdir,   'was terminated.')
        print('Termination process completed.')
    else:
        print('Termination process aborted.')
                    
if __name__ == '__main__':
    print('Terminator is a process, which looking for files with size\nbellow than pointed (aka "minimal_size"). Terminator will delete such files\n immediately. Be careful while using.\n Correct format of calling this file form shell: \npython3 Terminator.py <name_of_root_to_process> <minimal_size>\nRoot directory must contains full path.\n Minimal size pointed in bytes.')
    try:
        terminator(sys.argv[1],  sys.argv[2])
    except Exception:
        print('''Unexpected error. Use "python3 Terminator.py 
<name_of_root_directory_to_process> <minimal_size>" format of command.
Root directory must contains
 full path.\n Minimal size must be pointed in bytes.''')
        sys.exit()    
    
