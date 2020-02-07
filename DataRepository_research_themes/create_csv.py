import pandas as pd
import numpy as np
from urllib.error import URLError

def create_csv(url, outfile):
    """
    Purpose:
      This code generates a list of organization codes and associated portals

    :param url:
    :param outfile:
    :return:
    """
    # Read in URL that is of CSV format or CSV-exported
    try:
        df = pd.read_csv(url)
    except URLError:
        print("Unable to retrieve data from URL !")
        print("Please check your internet connection !")
        return

    # This will be the working copy that will be produced
    df_new = df.copy(deep=True)

    # Remove labels that we will not need
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
            sub_index = np.arange(overall_theme_index[i]+1, overall_theme_index[i+1])
        else:
            sub_index = np.arange(overall_theme_index[i]+1, df.shape[0])

        sub_portals    = df['Sub-portals'][sub_index]

        na_index = np.where(sub_portals.isna().values)[0]
        na_index = sub_index[na_index]
        df_new['Sub-portals'][na_index] = overall_theme_portal[i]
        df_new['Research Themes'][na_index] = overall_theme[i]

    # Remove entries for the overall theme
    df_new = df_new.drop(overall_theme_index)

    cols_order = ['Org Code',
                  'Sub-portals',
                  'Research Themes',
                  'Departments/Colleges/Labs/Centers',
                  'Parent Organization']
    df_new = df_new[cols_order]

    # Remove rows that do not contain an org code
    # final_rows = np.where(df_new['Org Code'].isna())[0]
    # df_new = df_new.drop(final_rows)

    # Write file
    df_new.to_csv(outfile, index=False)
