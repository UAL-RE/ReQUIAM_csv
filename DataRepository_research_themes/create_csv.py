import pandas as pd  # Currently using v0.25.3
import numpy as np   # Currently using v1.18.0
from urllib.error import URLError


def create_csv(url, outfile):
    """
    Purpose:
      This code generates a list of organization codes and associated portals
      for figshare account management.  The initial spreadsheet, which is
      curated by UA Libraries, is provided through the [url] input.

    :param url: Full url to CSV
    :param outfile: Exported file in CSV format
    :return:
    """

    # Read in URL that is of CSV format or CSV-exported (e.g., Google Sheets)
    try:
        df = pd.read_csv(url)
    except URLError:
        print("Unable to retrieve data from URL !")
        print("Please check your internet connection !")
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
    no_org_code = np.where(df_new['Org Code'].isna().values)[0]

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

    # Write file
    df_new.to_csv(outfile, index=False)
