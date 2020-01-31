import os
import json
import csv

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

from data import RAW_DATA, PROC_DATA, OUTPUT_CHARTS

WAVE_TYPE = {
    'longitudinal': 'p',
    'transverse': 's'
}

WATER_CONDITION = {
    '0': 'dry',
    '1': 'saturated'
}

def json_to_csv():
    dry_data_dir = RAW_DATA + '/waves/dry'
    sat_data_dir = RAW_DATA + '/waves/saturated'

    files = ['%s\%s' % (dry_data_dir, file) for file in os.listdir(dry_data_dir) if file.endswith(".json")]
    files = files + ['%s\%s' % (sat_data_dir, file) for file in os.listdir(sat_data_dir) if file.endswith(".json")]

    save_file = PROC_DATA + '/ultrasound_waves_data.csv'

    if os.path.exists(save_file):
        os.remove(save_file)

    with open(save_file, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows([[
            'sample_id', 'test_id', 'wave_type', 'test_condition', 'sampling_interval', 'sampling_unit', 'arrival_time', 'gain', 'amplitude', 'frequency', 'sampling'
        ]])
        for file in files:
            with open(file, "r") as read_file:
                test = json.load(file)

                for wave in test['waves']:
                    writer.writerows([[
                        test['id'],
                        wave['id'],
                        WAVE_TYPE[wave['type']],
                        WATER_CONDITION[waves['waterContent']],
                        wave['samplingInterval'],
                        wave['samplingUnit'],
                        wave['time1'],
                        wave['gain'],
                        wave['amplitude'],
                        wave['frequency'],
                        wave['data']
                    ]])

    csv_file.close()


def filter_tests(tests, sample_id=None, test_condition=None, wave_type=None):
    if (sample_id is not None):
        tests = tests.query('sample_id == "%s"' % sample_id)

    if (test_condition is not None):
        tests = tests.query('test_condition == "%s"' % test_condition)

    if (wave_type is not None):
        tests = tests.query('wave_type == "%s"' % wave_type)

    return tests


def waveform_plot(tests, ax_callback=None, plot_callback=None):
    grouped_tests = tests.groupby(['sample_id', 'test_condition', 'wave_type'])

    for index, test_group in grouped_tests:
        fig, axes = plt.subplots(len(test_group), 1, figsize=(20, 8 * len(test_group)))
        axes = np.array(axes).flatten().tolist()

        for test in test_group.itertuples():
            time = np.arange(0, len(test.sampling) * test.sampling_interval, test.sampling_interval)
            itime = np.arange(0, len(test.sampling) * test.sampling_interval, test.sampling_interval/5)
            cs = CubicSpline(time, test.sampling)

            ax = axes.pop(0)
            ax.axhline(color='black', linewidth=1)
            ax.plot(itime, cs(itime), '-b')
            ax.set_xlim([0, max(time)])
            ax.set_title('Teste ' + str(test.Index[3]))
            ax.set_ylabel('Amplitude')
            ax.set_xlabel('Tempo ($\mu$s)')

            if (ax_callback is not None):
                ax_callback(test, cs, ax)


        if (plot_callback is not None):
            plot_callback(index, test_group)

        plt.close()


def zero_crossing_threshold(wave, threshold, times_to_pick=4):
    time = np.arange(0, len(wave.sampling) * wave.sampling_interval, wave.sampling_interval)
    sampling = wave.sampling

    times_pos = CubicSpline(time, list(map(lambda a: a - threshold, sampling))).roots(extrapolate=False)
    times_neg = CubicSpline(time, list(map(lambda a: a + threshold, sampling))).roots(extrapolate=False)

    cs = CubicSpline(time, sampling)
    roots = cs.roots(extrapolate=False)

    all_times = [*times_pos, *times_neg]
    all_times.sort()

    arrival_times = []

    for t in all_times:
        lower = list(filter(lambda r: r < t, roots))

        if (len(lower) > 0):
            last = lower[-1]
            roots = list(filter(lambda r: r > last, roots))
            arrival_times.append(last)

        if (len(arrival_times) == times_to_pick):
            break

    return arrival_times


def first_break(wave, min_peak):
    time = np.arange(0, len(wave.sampling) * wave.sampling_interval, wave.sampling_interval)
    sampling = wave.sampling

    cs = CubicSpline(time, sampling)
    peaks = cs.derivative().roots(extrapolate=False)
    peaks = list(filter(lambda p: cs(p) > min_peak, peaks))
    peaks.sort()
    first_peak = peaks[0]

    roots = cs.roots(extrapolate=False)
    roots = list(filter(lambda r: r < first_peak, roots))
    roots.sort()
    first_break = roots[-1]

    return first_break

def mean_without_outliers(t, std_factor):
    if len(t) == 1:
        return t[0]

    mean = t.mean()
    std = t.std()
    std_range = [mean - std_factor * std, mean + std_factor * std]
    not_outliers = t[(t >= std_range[0]) & (t <= std_range[1])]

    return not_outliers.mean()