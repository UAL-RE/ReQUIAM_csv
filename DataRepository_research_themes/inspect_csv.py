import sys

import numpy as np

from .commons import no_org_code_index

import logging
formatter = logging.Formatter('%(levelname)s: %(message)s')
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)

# Index offset needed between pandas df and Google sheet
off = 2


class LogClass:

    def __init__(self, logdir):
        self.LOG_FILENAME = logdir + 'inspect_csv.log'
        self._log = self._get_logger()

    def _get_logger(self):
        log_level = logging.INFO
        log = logging.getLogger(self.LOG_FILENAME)
        if not getattr(log, 'handler_set', None):
            log.setLevel(logging.INFO)
            sh = logging.StreamHandler()
            sh.setFormatter(formatter)
            log.addHandler(sh)

            fh = logging.FileHandler(self.LOG_FILENAME)
            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)
            log.addHandler(fh)

            log.setLevel(log_level)
            log.handler_set = True
        return log


def inspect_csv(df):
    """
    Purpose:
      Inspects Google Sheet CSV-export table to identify issues.
      Minor issues are logged. Major issues prevent creating the
      final CSV file.

      Minor issues include:
       - Entries without an 'Org Code' (i.e., empty rows). Minor because
         it is excluded in final export

      Major issues include:
       - Duplicate entries based on Org Code
       - Invalid/incorrect entries in 'Departments/Colleges/Labs/Centers'
         This result in not getting a proper Org Code
       - Missing 'Research Themes' or Sub-portals if either one is provided
       - TBD

    :param df: pandas dataframe

    :return:
    """

    check = 0

    # MINOR INSPECTIONS

    # Check for entries without org code
    no_org_code = no_org_code_index(df)

    if no_org_code.size > 0:
        print("MINOR: Entries without Org Code found!")
        print("MINOR: Spreadsheet Index below:")
        array_str0 = np.array2string(no_org_code + off).split('\n')
        for arr_str in array_str0:
            print(arr_str)
    else:
        print("PASS: Org Code available for all entries!")

    # MAJOR INSPECTIONS

    # Check for number of unique cases
    not_na = df['Org Code'].loc[df['Org Code'].notna()]
    unique, unique_counts = np.unique(not_na, return_counts=True)
    n_dup = not_na.size - unique.size
    if n_dup == 0:
        print("PASS: No duplicate entries found!")
    else:
        print("MAJOR: Duplicate entries found, N={}!".format(n_dup))
        print("MAJOR: Please manually fix spreadsheet before proceeding!")
        print("MAJOR: Duplicate entries below:")
        print("MAJOR: Org Code : [Spreadsheet Index]")
        dup = np.where(unique_counts > 1)[0]
        for dd in dup:
            df_repeat = df.loc[df['Org Code'] == str(unique[dd])]
            print("   {} : {}".format(unique[dd], df_repeat.index.values+off))
        check += 1

    # Check that a valid Org Code is available when something is provided
    # in Departments field
    dept = df['Departments/Colleges/Labs/Centers']
    bad_idx = dept.notna() & df['Org Code'].isna()
    bad_dept = dept.loc[bad_idx]
    n_bad = bad_dept.size
    if n_bad == 0:
        print("PASS: No bad entries in Column E!")
    else:
        print("MAJOR: Entry in Column E is incorrect, N={}!".format(n_bad))
        print("MAJOR: Please manually fix spreadsheet before proceeding!")
        print("MAJOR: Bad entries below:")
        print("MAJOR: Department : [Spreadsheet Index]")
        for bb in bad_dept.index:
            print("   {} : {}".format(dept.loc[bb], bb + off))
        check += 1

    # Check that a valid Research Themes is available when Sub-portal is
    # provided and vice versa:
    rsh_theme  = df['Research Themes']
    sub_portal = df['Sub-portals']
    bad_theme_idx  = sub_portal.notna() & rsh_theme.isna()
    bad_portal_idx = rsh_theme.notna() & sub_portal.isna()

    bad_theme  = rsh_theme.loc[bad_theme_idx]
    bad_portal = rsh_theme.loc[bad_portal_idx]

    if bad_theme.size == 0:
        print("PASS: No bad entries in Column C!")
    else:
        print("MAJOR: Entry in Column C is unavailable, N={}!".format(bad_theme.size))
        print("MAJOR: Please manually fix spreadsheet before proceeding!")
        print("MAJOR: Bad entries below:")
        print("MAJOR: Portal : [Spreadsheet Index]")
        for bb in bad_theme.index:
            print("   {} : {}".format(sub_portal[bb], bb + off))
        check += 1

    if bad_portal.size == 0:
        print("PASS: No bad entries in Column D!")
    else:
        print("MAJOR: Entry in Column D is unavailable, N={}!".format(bad_portal.size))
        print("MAJOR: Please manually fix spreadsheet before proceeding!")
        print("MAJOR: Bad entries below:")
        print("MAJOR: Theme : [Spreadsheet Index]")
        for bb in bad_portal.index:
            print("   {} : {}".format(rsh_theme[bb], bb + off))
        check += 1

    if check != 0:
        raise ValueError
