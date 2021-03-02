import numpy as np
from pandas import DataFrame
from logging import Logger

from .commons import no_org_code_index

# Index offset needed between pandas df and Google sheet
off = 2


def inspect_csv(df: DataFrame, log: Logger):
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

    :param df: pandas dataframe
    :param log: A LogClass()._get_logger() object
    """

    check = 0

    # MINOR INSPECTIONS

    # Check for entries without org code
    no_org_code = no_org_code_index(df)

    if no_org_code.size > 0:
        log.info("MINOR: Entries without Org Code found!")
        log.info("MINOR: Spreadsheet Index below:")
        array_str0 = np.array2string(no_org_code + off).split('\n')
        for arr_str in array_str0:
            log.info(arr_str)
    else:
        log.info("PASS: Org Code available for all entries!")

    # MAJOR INSPECTIONS

    # Check for number of unique cases
    not_na = df['Org Code'].loc[df['Org Code'].notna()]
    unique, unique_counts = np.unique(not_na, return_counts=True)
    n_dup = not_na.size - unique.size
    if n_dup == 0:
        log.info("PASS: No duplicate entries found!")
    else:
        log.warning(f"MAJOR: Duplicate entries found, N={n_dup}!")
        log.warning("MAJOR: Please manually fix spreadsheet before proceeding!")
        log.warning("MAJOR: Duplicate entries below:")
        log.warning("MAJOR: Org Code : [Spreadsheet Index]")
        dup = np.where(unique_counts > 1)[0]
        for dd in dup:
            df_repeat = df.loc[df['Org Code'] == str(unique[dd])]
            log.info(f"   {unique[dd]} : {df_repeat.index.values + off}")
        check += 1

    # Check that a valid Org Code is available when something is provided
    # in Departments field
    dept = df['Departments/Colleges/Labs/Centers']
    bad_idx = dept.notna() & df['Org Code'].isna()
    bad_dept = dept.loc[bad_idx]
    n_bad = bad_dept.size
    if n_bad == 0:
        log.info("PASS: No bad entries in Column E!")
    else:
        log.warning(f"MAJOR: Entry in Column E is incorrect, N={n_bad}!")
        log.warning("MAJOR: Please manually fix spreadsheet before proceeding!")
        log.warning("MAJOR: Bad entries below:")
        log.warning("MAJOR: Department : [Spreadsheet Index]")
        for bb in bad_dept.index:
            log.info(f"   {dept.loc[bb]} : {bb + off}")
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
        log.info("PASS: No bad entries in Column C!")
    else:
        log.warning(f"MAJOR: Entry in Column C is unavailable, N={bad_theme.size}!")
        log.warning("MAJOR: Please manually fix spreadsheet before proceeding!")
        log.warning("MAJOR: Bad entries below:")
        log.warning("MAJOR: Portal : [Spreadsheet Index]")
        for bb in bad_theme.index:
            log.info(f"   {sub_portal[bb]} : {bb + off}")
        check += 1

    if bad_portal.size == 0:
        log.info("PASS: No bad entries in Column D!")
    else:
        log.warning(f"MAJOR: Entry in Column D is unavailable, N={bad_portal.size}!")
        log.warning("MAJOR: Please manually fix spreadsheet before proceeding!")
        log.warning("MAJOR: Bad entries below:")
        log.warning("MAJOR: Theme : [Spreadsheet Index]")
        for bb in bad_portal.index:
            log.info(f"   {rsh_theme[bb]} : {bb + off}")
        check += 1

    if check != 0:
        raise ValueError
