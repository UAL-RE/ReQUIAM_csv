import pandas as pd
import numpy as np


def create_csv(url, outfile):
    """
    Purpose:
      This code generates a list of organization codes and associated portals

    :param url:
    :param outfile:
    :return:
    """
    # Read in URL that is of CSV format or CSV-exported
    df = pd.read_csv(url)

    # Retrieve overall themes, corresponding portal and entries
    overall_theme0        = df['Overall Themes']
    overall_theme_portal0 = df['Overall Themes Portal']

    # Identify rows associated with overall themes
    overall_theme_index = np.where(overall_theme0.notna().values)[0]

    overall_theme        = overall_theme0.values[overall_theme_index]
    overall_theme_portal = overall_theme_portal0.values[overall_theme_index]

    portal_names = np.array([''] * df.shape[0])

    # Identify portal for each university organization
    for i in range(len(overall_theme)):
        if i != len(overall_theme)-1:
            sub_index = np.arange(overall_theme_index[i]+1, overall_theme_index[i+1])
        else:
            sub_index = np.arange(overall_theme_index[i]+1, df.shape[0])

        research_theme = df['Research Themes'][sub_index]
        sub_portals    = df['Sub-portals'][sub_index]

        na_index   = np.where(sub_portals.isna().values)[0]
        na_index   = sub_index[na_index]
        portal_names[na_index] = overall_theme_portal[i]

        uniq_index = np.where(sub_portals.notna().values)[0]
        portal_names[sub_index[uniq_index]] = sub_portals[uniq_index]

    print(portal_names)
