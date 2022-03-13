"""
In this script you can choose directory for seeking and
the lowest available size. Files with lower size will be deleted.

You can use it by shell: "python3 Terminator.py <tree_path> <minimal_size in bytes>"

Created by Nick Kanah.

"""
# TODO: актуализировать ^ и README !

import os
import sys
from enum import Enum
from typing import List, Any



class ComparingType(str, Enum):
    is_ = 'is'
    lower = 'lower'
    bigger = 'bigger'


class AvailableCriteria(str, Enum):
    extension = 'file_extension', 'expected value: string without dots'
    size = 'file_size', 'expected value: number of bytes'

    def __new__(cls, value, description):
        obj = str.__new__(cls, value)
        obj._value_ = value

        obj.description = description
        return obj


list_of_criteria_info = [criteria.value+f"({criteria.description})" for criteria in AvailableCriteria]


def request_confirmation(list_of_file_names: List[str]):
    # TODO docs
    print('Next files matching the criteria were found:')
    for filename in list_of_file_names:
        print('\n'+filename)
    while True:
        answer = input('Would you like to terminate these files? \n[Y]es or [N]o.')
        if answer in ['Y', 'y']:
            return True
        if answer in ['N', 'n']:
            return False
        else:
            print('Incorrect answer. Please, enter "y" for "yes" or "n" for "no".')


def is_meets_criteria(
        file_name: str,
        criteria: AvailableCriteria,
        criteria_value: Any,
        comparing_type: str,
) -> bool:
    """Checks if file meets designated criteria.

    :param file_name: the name of file. Must not contain path elements.
    :type file_name: str

    :param criteria: the type of criteria, by which one files are filtered.
    :type criteria: AvailableCriteria

    :param criteria_value: the value of criteria. For example, size in bytes.
    :type criteria_value: Any

    :param comparing_type: is(=), lower or bigger
    :type comparing_type: str
    :return:
    """

    if criteria not in AvailableCriteria._member_map_.values():
        raise ValueError(
            f"Incorrect criteria was given! Available criteria:\n{f'{AvailableCriteria.values()}'}")

    if comparing_type not in ComparingType._member_map_.values():
        raise ValueError(
            f"Incorrect comparing_type was given! Available comparing_type's:\n{f'{ComparingType.values()}'}")
    # TODO: cfh
    # stats = os.stat(fullFilePath)
    # if stats.st_size < minimal_size:


def terminator(root_directory_path, criteria, criteria_value, comparing_type):

    termination_list = []

    for (this_dir, sub_dirs, files_here) in os.walk(root_directory_path):
        for file_name in files_here:
            if file_name != 'Terminator.py':
                if is_meets_criteria(file_name, criteria, criteria_value, comparing_type):
                    termination_list.append(os.path.join(this_dir, file_name))

    # TODO: cfh
    if request_confirmation(termination_list) == True:
        try:
            for file_name in termination_list:
                os.remove(file_name)
        except Exception:
            print('WARNING!\nSome unknown error was occured:',  sys.exc_info())
        except PermissionError:  
            print('WARNING!\nTermination of file', fullFilePath, 'is not permitted. File skipped.')
        else:
            print('File', str(file_name), 'from directory', this_dir, 'was terminated.')
        print('Termination process completed.')
    else:
        print('Termination process aborted.')


if __name__ == '__main__':

    ####################################################################################################
    print(
        'Terminator is a script, which looking for files which are meet\n'
        'the criteria that pointed. Terminator will find such files\n'
        ' and show you the list of them. If you will be agree, the script will delete them.\n'
        'Be careful while using.\n'
        'Correct format of calling this script using shell:\n'
        'python3 Terminator.py <root_directory_to_process> <criteria> <value> <comparing_type>\n\n'
        '· root_directory_to_process - must be a full path.\n'
        '· criteria - is the attribute of file which we are using to decide if it will be deleted or not.\n'
        'Available criteria for now:'
    )
    for criteria in list_of_criteria_info:
        print(f'\t- {criteria}')
    print(
        '\n· value - the value of criteria.\n\n'
        '· comparing_type - the way to compare values. Available comparing types:'
    )
    for c_type in ComparingType:
        print(f'\t- {c_type}')
    ####################################################################################################
    if len(sys.argv) < 5:
        print('\n\nNot all required arguments were passed. Read description above.\nAborting.')
        sys.exit(0)
    try:
        terminator(
            root_directory_path=sys.argv[1],
            criteria=sys.argv[2],
            criteria_value=sys.argv[3],
            equality=sys.argv[4]
        )
    except Exception:
        print(
            'Unexpected error:',
            sys.exc_info(),
        )
        sys.exit()    
