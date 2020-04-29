import os
import pandas as pd


def join_data_preprocessing():
    """ Gets data from the files and joins them on pat_id into a single file
    """

    path_dir = os.environ.get('DATA_DIR', '/data/')

    file_admission_loc = os.environ.get('FILE_ADMISSION', 'admission.csv')
    file_age_loc = os.environ.get('FILE_AGE', 'age.csv')
    file_signal_loc = os.environ.get('FILE_SIGNAL', 'signal.csv')

    # read from CSV
    df_age = pd.read_csv(os.path.join(path_dir, file_age_loc), sep=';', usecols=[1, 2])
    df_adm = pd.read_csv(os.path.join(path_dir, file_admission_loc), sep=';', usecols=[1, 2, 3])
    df_sig = pd.read_csv(os.path.join(path_dir, file_signal_loc), sep=';', usecols=[2, 3, 4, 5, 6])

    # JOIN
    df_aa = pd.merge(df_adm, df_age, on='pat_id')
    df_aas = pd.merge(df_aa, df_sig, on='pat_id')

    # KEEP DATE IN ORDER (simulates real stream)
    df_aas.sort_values(['day', 'hour'], inplace=True)

    file_all_joined = os.path.join(path_dir, os.environ.get('FILE_ALL', 'all_data.csv'))
    df_aas.to_csv(file_all_joined, sep=';', encoding='utf-8')

    return 'Ok'