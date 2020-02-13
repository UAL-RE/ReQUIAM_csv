from os import path
import pandas as pd  # Currently using v0.25.3
import numpy as np   # Currently using v1.18.0
from urllib.error import URLError

co_filename = __file__
co_dir = path.dirname(co_filename)

# Index offset needed between pandas df and Google sheet
off = 2

# class TableError(Exception):
#    """Base class for table exceptions"""
#    pass
#
#    # def __init__(self, message):
#    #       self.message = "pass


def no_org_code_index(df):
    """
    Purpose:
      Identify entries without an Org Code.  This is based on whether
      the value is set to NaN

    :param df: pandas dataframe
    :return no_org_code: numpy array containing elements
    """

    no_org_code = np.where(df['Org Code'].isna() &
                           df['Overall Themes'].isna())[0]

    return no_org_code


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
        print("MINOR: Index below:")
        array_str0 = np.array2string(no_org_code).split('\n')
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


def create_csv(url, outfile):
    """
    Purpose:
      This code generates a list of organization codes and associated
      portals for figshare account management.
       - The initial spreadsheet, which is curated by UA Libraries, is
         provided through the [url] input.
       - The exported CSV file will be placed in this git repo. Current
         path and file preference:
           DataRepository_research_themes/data/research_themes.csv

    :param url: Full url to CSV
    :param outfile: Exported file in CSV format
    """

    # Read in URL that is of CSV format or CSV-exported (e.g., Google Sheets)
    try:
        df = pd.read_csv(url)
    except URLError:
        print("Unable to retrieve data from URL !")
        print("Please check your internet connection !")
        return

    try:
        inspect_csv(df)
    except ValueError:
        print("ERROR: Table is not correctly formatted!")
        print("ERROR: Check the logs for explanations")
        return

    # This will be the working copy that will be produced
    df_new = df.copy(deep=True)

    # Remove unused columns
    drop_labels = ['Overall Themes',
                   'Overall Themes Portal',
                   'Departments/Colleges/Labs/Centers (Old)',
                   'Additional Information']
    df_new = df_new.drop(labels=drop_labels, axis=1)

    # Retrieve overall themes, corresponding portal and entries
    overall_theme0        = df['Overall Themes']
    overall_theme_portal0 = df['Overall Themes Portal']

    # Identify rows associated with overall themes
    overall_theme_index = np.where(overall_theme0.notna().values)[0]

    overall_theme        = overall_theme0.values[overall_theme_index]
    overall_theme_portal = overall_theme_portal0.values[overall_theme_index]

    # Identify portal for each university organization
    for i in range(len(overall_theme)):
        print("# Working on {}".format(overall_theme[i]))

        if i != len(overall_theme)-1:
            sub_index = np.arange(overall_theme_index[i]+1,
                                  overall_theme_index[i+1])
        else:
            sub_index = np.arange(overall_theme_index[i]+1,
                                  df.shape[0])

        sub_portals = df['Sub-portals'][sub_index]

        na_index = np.where(sub_portals.isna().values)[0]
        na_index = sub_index[na_index]
        df_new['Sub-portals'][na_index] = overall_theme_portal[i]
        df_new['Research Themes'][na_index] = overall_theme[i]

    # Identify rows that do not contain an org code
    no_org_code = no_org_code_index(df_new)

    # Remove entries without org code. This ensures that the overall theme are ignored
    concat_rows = np.concatenate((overall_theme_index, no_org_code))
    drop_rows = np.unique(concat_rows)

    df_new = df_new.drop(drop_rows)

    # Re-order columns
    cols_order = ['Org Code',
                  'Sub-portals',
                  'Research Themes',
                  'Departments/Colleges/Labs/Centers',
                  'Parent Organization']
    df_new = df_new[cols_order]

    # Write file.  File is placed within the git repository
    df_new.to_csv(path.join(co_dir, outfile), index=False)
