import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv(r'C:\Users\bruno\OneDrive\Área de Trabalho\atividade3-python\boilerplate-medical-data-visualizer\medical_examination.csv')

# 2


# Calculate BMI
df['BMI'] = df['weight'] / ((df['height'] / 100) ** 2)

df['overweight'] = (df['BMI'] > 25).astype(int)

# 3
df['cholesterol'] = df['cholesterol'].apply(lambda x: 1 if x > 1 else 0)
df['gluc'] = df['gluc'].apply(lambda x: 1 if x > 1 else 0)

# 4
def draw_cat_plot():
# Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])

    # Group and reformat the data to split it by 'cardio' levels
    df_cat = df_cat.groupby(['variable', 'value', 'cardio'])['value'].count().reset_index(name='total')

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(x="variable", y="total", hue="value", col="cardio", data=df_cat, kind="bar", height=6, aspect=1)

    # Set the labels
    fig.set_axis_labels("variable", "total")
    fig.set_titles("cardio = {col_name}")

    # Get the figure for returning
    fig = fig.fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig

def draw_heat_map():
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & 
                 (df['height'] >= df['height'].quantile(0.025)) &
                 (df['height'] <= df['height'].quantile(0.975)) & 
                 (df['weight'] >= df['weight'].quantile(0.025)) & 
                 (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix without the 'BMI' column
    corr = df_heat.drop(columns=['BMI']).corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(11, 9))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask=mask, annot=True, fmt='.1f', square=True, linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig