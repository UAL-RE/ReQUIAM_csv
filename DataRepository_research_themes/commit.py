from os import path
from os import system
import configparser

co_filename = __file__
co_dir = path.dirname(co_filename)


def awk_message(execute=False):

    # Parse configuration from default.ini
    config = configparser.ConfigParser()
    config.read(path.join(co_dir, 'default.ini'))

    outfile_dir  = config.get('global', 'outfile_dir')
    outfile_dir0 = path.join(co_dir, outfile_dir)

    ref_file = path.join(outfile_dir0, config.get('global', 'outfile'))

    if not execute:
        new_file = path.join(outfile_dir0, config.get('global', 'outfile_dryrun'))

        awk_cmd  = f'diff {ref_file} {new_file} | grep ">" | '
        awk_cmd += 'awk \'BEGIN{FS=","}; {sub(/>/,""); printf("%6s %s\\n", $1, $4)}\''
        print(awk_cmd)
        system(awk_cmd)
        print(f"git add {ref_file}")
    else:
        print("Cannot get commit message (for now)")
