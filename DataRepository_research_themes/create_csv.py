from os import path
import pandas as pd  # Currently using v0.25.3
import numpy as np   # Currently using v1.18.0
from urllib.error import URLError

from .inspect_csv import inspect_csv
from .commons import no_org_code_index

from datetime import datetime as dt

co_filename = __file__
co_dir = path.dirname(co_filename)


def create_csv(url, outfile, log):
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
    :param log: LogClass.get_logger() object
    """

    t_start = dt.now()

    # Read in URL that is of CSV format or CSV-exported (e.g., Google Sheets)
    try:
        df = pd.read_csv(url)
    except URLError:
        log.warning("Unable to retrieve data from URL !")
        log.warning("Please check your internet connection !")
        return

    try:
        inspect_csv(df, log)
    except ValueError:
        log.warning("Table is not correctly formatted!")
        log.warning("Check the logs for explanations")
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
        log.info("# Working on {}".format(overall_theme[i]))

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
    no_org_code = no_org_code_index(df)

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

    t_stop = dt.now()

    delta = t_stop - t_start
    sec = delta.seconds
    HH = sec // 3600
    MM = (sec // 60) - (HH * 60)
    SS = sec - (HH * 3600) - (MM * 60)
    t_format = "Total time: {} hours  {} minutes  {} seconds".format(HH, MM, SS)
    log.info(t_format)
