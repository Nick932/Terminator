'''''''''
In this scrpit you can choose directories for seeking and
necessary size of files to delete them.

Created by Nickel.

'''''''''


import os
import traceback

amount=68 # how much directories would you like to research?

dirs_names=[str(x) for x in range(amount)] 




pa='/media/user/USB DISK/recup_dir.2' # put here one of paths
paths=[]                                # put here list of them, or...

#____________________________________________________________________________#
# ... because names of directories have difference in only last one digital, 
# I generate all directory's paths using this way:

count=2 # I started with '2' because my first directory (pa) ends with 2.
while len(paths)<amount: 
    x=pa[:-1]
    x=x+str(count)
    count+=1
    paths.append(x)

minimal_size=118000 # in bytes. EACH SMALLER FILE WILL BE DELETED!
#____________________________________________________________________________#


#######################TERMINATION PROCESS#####################################

for each in paths:
    try:
        files=os.listdir(each)
    
        for file in files:
            if file!='terminator.py':
                statinfo = os.stat(str(each)+'/'+str(file))
                if statinfo.st_size<minimal_size:
                    os.remove(str(each)+'/'+str(file))
                    print('"'+file+'"', 'TERMINATED from directory:',
                          '\n',each, '\n')
    except FileNotFoundError:
        print('______________________________' '\n', '\n', 
        "some directories which was add to paths dosn't exist:")
        doesnt=(str(traceback.format_exc().rstrip()))
        doesnt=doesnt.split('directory:')
        exces=doesnt[1]
        print(exces, '\n', '______________________________', '\n')

print('Termination status: complete.')   
    
    
