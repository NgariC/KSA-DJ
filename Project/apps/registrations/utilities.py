import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from apps.core.project_requirements.utilities import get_graph

SECTION = (
    ('Sungura', 'Sungura'),
    ('Chipukizi', 'Chipukizi'),
    ('Mwamba', 'Mwamba'),
    ('Jasiri', 'Jasiri'),
)

TRAINING = (
    ('Not Yet Trained', 'Not Yet Trained'),
    ('ITC', 'ITC'),
    ('PTC', 'PTC'),
    ('WB Theory', 'WB Theory'),
    ('WB Course', 'WB Course'),
    ('WB Assessment', 'WB Assessment'),
    ('Two Beads', 'Two Beads'),
    ('ALT Course', 'ALT Course'),
    ('ALT Project', 'ALT Project'),
    ('Three Beads', 'Three Beads'),
    ('LT Course', 'LT Course'),
    ('LT Project', 'LT Project'),
    ('Four Beads', 'Four Beads'),
)


def u_code(pk):
    if not pk:
        return "00000"
    if len(str(pk)) == 1:
        return f"0000{pk}"
    elif len(str(pk)) == 2:
        return f"000{pk}"
    elif len(str(pk)) == 3:
        return f"00{pk}"
    elif len(str(pk)) == 4:
        return f"0{pk}"
    else:
        return f"{pk}"


def unit_chart(df, level, model):
    plt.switch_backend('AGG')
    plt.subplots()
    fig = plt.figure(figsize=(16, 9))

    x = df[level]
    y1 = df[f'{model}']
    y2 = df['Sungura']
    y3 = df['Chipukizi']
    y4 = df['Mwamba']
    y5 = df['Jasiri']
    width = 0.275
    z = np.arange(len(df))

    plt.plot(x, y1, label='Totals', color='black', marker='o', linestyle='dashed')
    plt.bar(z - width, y2, width=width, color='#FFFF33', label='Sungura')
    plt.bar(z - width / 2, y3, width=width, color='#006400', label='Chipukizi')
    plt.bar(z + width / 2, y4, width=width, color='#8B0000', label='Mwamba')
    plt.bar(z + width, y5, width=width, color='#FD6A02', label='Jasiri')
    if level == 'Region':
        plt.title(f'{model.upper()} PER {level.upper()}S', fontsize=20)
        plt.xlabel(f'{level.upper()}S', fontsize=14)
    elif level == 'County':
        plt.title(f'{model.upper()} PER COUNTIES', fontsize=20)
        plt.xlabel('COUNTIES', fontsize=14)
    elif level == 'SubCounty':
        plt.title(f'{model.upper()} PER SUBCOUNTIES', fontsize=20)
        plt.xlabel('SUBCOUNTIES', fontsize=14)
    plt.ylabel(model.upper(), fontsize=14)
    plt.legend()
    plt.xticks(rotation=90)
    plt.tight_layout()
    return get_graph()


def unit_table(df, summary_total, level, model):
    new_row = pd.Series(data={f'{level}': 'Total',
                              'Sungura': summary_total.get('sungura_total'),
                              'Chipukizi': summary_total.get('chipukizi_total'),
                              'Mwamba': summary_total.get('mwamba_total'),
                              'Jasiri': summary_total.get('jasiri_total'),
                              f'{model}': summary_total.get('total'),
                              'Percentage': '100% of Total'}, name='-')
    df['Percentage'] = round((df.get(model) / summary_total.get('total') * 100), 2)
    df.index = np.arange(1, len(df) + 1)
    df = df.append(new_row, ignore_index=False)
    return df.to_html(border=0, classes='totals')


def scouts_chart(df, level, model):
    plt.switch_backend('AGG')
    plt.subplots()
    fig = plt.figure(figsize=(16, 9))

    x = df[level]
    y1 = df[f'{model}']
    y2 = df['Male']
    y3 = df['Female']
    width = 0.4
    z = np.arange(len(df))

    plt.plot(x, y1, label='Totals', color='red', marker='o', linestyle='dashed')
    plt.bar(z - (width / 2), y2, width=width, color='blue', label='Male')
    plt.bar(z + (width / 2), y3, width=width, color='pink', label='Female')
    if level == 'Region':
        plt.title(f'{model.upper()} PER {level.upper()}S', fontsize=20)
        plt.xlabel(f'{level.upper()}S', fontsize=14)
    elif level == 'County':
        plt.title(f'{model.upper()} PER COUNTIES', fontsize=20)
        plt.xlabel('COUNTIES', fontsize=14)
    elif level == 'SubCounty':
        plt.title(f'{model.upper()} PER SUBCOUNTIES', fontsize=20)
        plt.xlabel('SUBCOUNTIES', fontsize=14)
    plt.ylabel(model.upper(), fontsize=14)
    plt.legend()
    plt.xticks(rotation=90)
    plt.tight_layout()
    return get_graph()


def scouts_table(df, summary_total, level, model):
    new_row = pd.Series(data={f'{level}': 'Total',
                              'Male': summary_total.get('male_total'),
                              'Female': summary_total.get('female_total'),
                              f'{model}': summary_total.get('total'),
                              'Percentage': '100% of Total'}, name='-')
    df['Percentage'] = round((df.get(model) / summary_total.get('total') * 100), 2)
    df.index = np.arange(1, len(df) + 1)
    df = df.append(new_row, ignore_index=False)
    df.insert(2, 'M-%', round((df.get('Male') / summary_total.get('male_total') * 100)), 2)
    df.insert(4, 'F-%', round((df.get('Female') / summary_total.get('female_total') * 100)), 2)
    return df.to_html(border=0, classes='totals')
