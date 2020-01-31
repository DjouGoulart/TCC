import os
import pandas as pd
import numpy as np

RAW_DATA = os.path.abspath(os.path.join('../data/raw'))
PROC_DATA = os.path.abspath(os.path.join('../data/processed'))
OUTPUT_CHARTS = os.path.abspath(os.path.join('../output/charts'))

def get_data():
    df = pd.read_excel(PROC_DATA + '/samples.xlsx', sheet_name='dataframe', index_col=0)
    df = df.infer_objects()

    lithos = ['Basalto Maciço', 'Basalto Vesiculado', 'Basalto Brechado', 'Basalto Hidrotermal', 'Peperito', 'Riolito', 'Arenito']
    df['litologia'] = pd.Categorical(df['litologia'], lithos)
    df = df.sort_values(by='litologia')

    return df

meta = {
    'p_esp_seco': {
        'limits': np.array([19, 30]),
        'unit': 'kN/m^3',
        'symbol': '\gamma_{seco}'
    },
    'p_esp_sat': {
        'limits': np.array([20, 30]),
        'unit': 'kN/m^3',
        'symbol': '\gamma_{sat}'
    },
    'teor_umidade': {
        'limits': np.array([0, 10]),
        'unit': '\%',
        'symbol': 'w'
    },
    'porosidade_efetiva': {
        'limits': np.array([0, 20]),
        'unit': '\%',
        'symbol': 'n_e'
    },
    'vp_seco': {
        'limits': np.array([2, 7]),
        'unit': 'km/s',
        'symbol': 'V_{p\_seco}'
    },
    'vs_seco': {
        'limits': np.array([1.5, 3.5]),
        'unit': 'km/s',
        'symbol': 'V_{s\_seco}'
    },
    'e_din_seco': {
        'limits': np.array([0, 100]),
        'unit': 'GPa',
        'symbol': 'E_{din\_seco}'
    },
    'poisson_din_seco': {
        'limits': np.array([0, 0.5]),
        'unit': None,
        'symbol': '\\nu_{din\_seco}'
    },
    'vp_sat': {
        'limits': np.array([3, 7]),
        'unit': 'km/s',
        'symbol': 'V_{p\_sat}'
    },
    'vs_sat': {
        'limits': np.array([1, 4]),
        'unit': 'km/s',
        'symbol': 'V_{s\_sat}'
    },
    'e_din_sat': {
        'limits': np.array([0, 100]),
        'unit': 'GPa',
        'symbol': 'E_{din\_sat}'
    },
    'poisson_din_sat': {
        'limits': np.array([0, 0.5]),
        'unit': None,
        'symbol': '\\nu_{din\_sat}'
    },
    'e_est_sat': {
        'limits': np.array([0, 120]),
        'unit': 'GPa',
        'symbol': 'E_{est\_sat}'
    },
    'ucs': {
        'limits': np.array([0, 300]),
        'unit': 'MPa',
        'symbol': '\sigma_c'
    }
}