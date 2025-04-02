import marimo

__generated_with = "0.12.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import marimo as mo
    return mo, pd


@app.cell
def _(pd):
    df = pd.read_csv('./data.csv')
    df.sample(n = 10)
    return (df,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Preprocessing the dataset
        We will preprocess the data by removing records that do not have a `disease_area` attribute.
        """
    )
    return


@app.cell
def _(df):
    proc_df = df.dropna().assign(disease_area=df['disease_area'].str.replace('/', '|').str.split('|')).explode('disease_area')
    proc_df.sample(n = 10)
    return (proc_df,)


@app.cell
def _(mo):
    mo.md(r"""Now, we notice that the `indication` attribute often has multiple disease names like such 'disease1|disease2'. So, we will replace rows like these by splitting them into multiples.""")
    return


@app.cell
def _(df, proc_df):
    augmented_df = proc_df.assign(indication=df['indication'].str.split('|')).explode('indication')
    augmented_df.sample(n = 10)
    return (augmented_df,)


@app.cell
def _(mo):
    mo.md(r"""Since, we are only concerned with the disease and the corresponding drugs, we will extract those from the processed data.""")
    return


@app.cell
def _(augmented_df):
    principal_df = augmented_df[['indication', 'pert_iname']]
    principal_df.sample(n = 10)
    return (principal_df,)


@app.cell
def _(mo):
    disease_input = mo.ui.text(label="Disease", placeholder="Search...")
    find_button = mo.ui.run_button(label="Find drugs")
    mo.md(f"{disease_input}")
    mo.hstack([disease_input, find_button])
    return disease_input, find_button


@app.cell
def _(disease_input, find_button, principal_df):
    if find_button.value:
        print(principal_df[principal_df['indication'] == disease_input.value]['pert_iname'].unique().tolist())
    return


@app.cell
def _(df):
    df.clinical_phase.unique()
    return


@app.cell
def _(augmented_df):
    augmented_df['moa'].unique()

    return


if __name__ == "__main__":
    app.run()
