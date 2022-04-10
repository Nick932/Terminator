"""
Terminator is a script, which is looking for files meets
the pointed criteria. Terminator will find and show
such files to you. If you agree, the script will delete them.

Copyleft 2020 Nick Kanah. Knowledge must be free.
"""

import os
import sys
from enum import Enum
from pathlib import Path
from typing import List, Any


class ComparingType(str, Enum):
    equal = 'equal'
    lower = 'lower'
    bigger = 'bigger'


class AvailableCriteria(str, Enum):
    extension = 'file_extension', 'expected value: string without dots'
    size = 'file_size', 'expected value: size in bytes'

    def __new__(cls, value, description):
        obj = str.__new__(cls, value)
        obj._value_ = value

        obj.description = description
        return obj


list_of_criteria_info = [criteria.value+f"({criteria.description})" for criteria in AvailableCriteria]
list_of_comparing_types = [comparing_type.value for comparing_type in ComparingType]


def is_deletion_confirmed(list_of_file_names: List[str]):
    """Asks the user if he wants to delete the found files."""
    print('\nNext files matching the criteria were found:')
    list_of_file_names.sort()
    for filename in list_of_file_names:
        print('\n'+filename)
    while True:
        answer = input('Would you like to terminate these files? \n[Y]es or [N]o.\n')
        if answer in ['Y', 'y']:
            return True
        if answer in ['N', 'n']:
            return False
        else:
            print('Incorrect answer. Please, enter "y" for "yes" or "n" for "no".')


def is_value_meets_required(current_value: Any, required_value: Any, comparing_type: ComparingType) -> bool:
    if comparing_type == ComparingType.lower:
        return current_value < required_value
    if comparing_type == ComparingType.bigger:
        return current_value > required_value
    if comparing_type == ComparingType.equal:
        return current_value == required_value


def is_meets_criteria(
        path_to_file: str,
        criteria: AvailableCriteria,
        criteria_value: Any,
        comparing_type: ComparingType,
) -> bool:
    """Checks if file meets designated criteria.

    :param path_to_file: the full path to file.
    :type path_to_file: str

    :param criteria: the type of criteria, by which one files are filtered. For example, 'size'
    :type criteria: AvailableCriteria

    :param criteria_value: the value of criteria. For example, int-type value (size in bytes).
    :type criteria_value: Any

    :param comparing_type: equal, lower or bigger
    :type comparing_type: str

    :rtype: bool
    """
    result = False

    if criteria not in AvailableCriteria._member_map_.values():
        raise ValueError(
            f"Incorrect criteria was given! Available criteria:\n{list_of_criteria_info}")

    if comparing_type not in ComparingType._member_map_.values():
        raise ValueError(
            "Incorrect comparing_type was given! "
            f"Available comparing_type's:\n{list_of_comparing_types}")

    if criteria == AvailableCriteria.size.value:
        file_size = os.stat(path_to_file).st_size
        result = is_value_meets_required(
            current_value=int(file_size),
            required_value=int(criteria_value),
            comparing_type=comparing_type,
        )
    elif criteria == AvailableCriteria.extension.value:
        file_extension = Path(path_to_file).suffix[1:]
        result = is_value_meets_required(
            current_value=str(file_extension),
            required_value=criteria_value,
            comparing_type=comparing_type,
        )

    return result


def terminator(root_directory_path: str, criteria, criteria_value, comparing_type):

    """
    :param root_directory_path: the full path to file.
    :type root_directory_path: str

    :param criteria: the type of criteria, by which one files are filtered. For example, 'size'
    :type criteria: AvailableCriteria

    :param criteria_value: the value of criteria. For example, int-type value (size in bytes).
    :type criteria_value: Any

    :param comparing_type: equal, lower or bigger
    :type comparing_type: str

    """

    termination_list = []

    for (this_dir, sub_dirs, files_here) in os.walk(root_directory_path):
        for file_name in files_here:
            if file_name != 'terminator.py':
                full_path_to_file = Path(this_dir) / file_name
                if is_meets_criteria(full_path_to_file, criteria, criteria_value, comparing_type):
                    termination_list.append(str(full_path_to_file))

    if not termination_list:
        print('Files matching the criteria were not found. Aborting.')
        sys.exit(0)

    if is_deletion_confirmed(termination_list):

        for full_path_to_file in termination_list:

            try:
                os.remove(full_path_to_file)
            except Exception:
                print('ERROR!\nSome unknown error was occured:\n',  sys.exc_info())
            except PermissionError:
                print(f'WARNING!\nTermination of file {full_path_to_file} is not permitted. File skipped.')

            else:

                file_name = Path(full_path_to_file).name
                if file_name[:4].upper() == 'SARA':
                    print('\n|ఠ‗ఠ| ︻デ═一\n- Sara Connor?')

                print(f'File {full_path_to_file} was terminated.\n')

        print('\nTermination process completed.')

    else:
        print('\nFiles were not deleted. Termination process aborted.')


this_file_name_string = os.path.basename(__file__)
root_directory_to_process_string = 'root_directory_to_process'
criteria_string = 'criteria'
value_string = 'value'
comparing_type_string = 'comparing_type'


def docs():
    print(
        '\nTerminator is a script, which is looking for files meets\n'
        'the pointed criteria. Terminator will find and show\n'
        'such files to you. If you agree, the script will delete them.\n'
        '\nBe careful while using.\n\n'
        'Correct format of calling this script using shell:\n'
        f'python3 {this_file_name_string} <{criteria_string}> <{value_string}> <{comparing_type_string}> '
        f'<{root_directory_to_process_string}>\n\n'
        f'· {criteria_string} - the attribute of file which we are using to decide if it will be deleted or not.\n'
        '  Available criteria for now:'
    )
    for criteria in list_of_criteria_info:
        print(f'\t- {criteria}')
    print(
        f'\n· {value_string} - the value of criteria. For example: txt\n\n'
        f'· {comparing_type_string} - the way to compare values. Available comparing types:'
    )
    for c_type in ComparingType:
        print(f'\t- {c_type}')

    print(
        f'\n· {root_directory_to_process_string} - optional argument, '
        f'must be a full path (no slash at the end). \n'
        f'  By default - current directory of {this_file_name_string}\n'
    )


if __name__ == '__main__':

    if len(sys.argv) < 4:

        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '-H', '--help']:
            docs()
            sys.exit(0)

        docs()
        print(
            '\n\nNot all required arguments were passed while calling the script.\n'
            'Read the description above.\n'
            'Correct format of calling this script using shell:\n'
            f'python3 {this_file_name_string} <{criteria_string}> <{value_string}> '
            f'<{comparing_type_string}> <{root_directory_to_process_string}>\n\n'
        )
        sys.exit(0)

    the_path = os.getcwd() if len(sys.argv) < 5 else sys.argv[4]
    if the_path[-1] == "/":
        the_path = the_path[:-1]

    terminator(
        criteria=sys.argv[1],
        criteria_value=sys.argv[2],
        comparing_type=sys.argv[3],
        root_directory_path=the_path,
    )
