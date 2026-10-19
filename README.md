# Islamabad House Price Predictor

Estimate the price of a residential property in Islamabad using its location,
area, bedroom count, and bathroom count. The app wraps a trained
`DecisionTreeRegressor` in a simple Streamlit interface.

## Try the live app

**[Open the Islamabad House Price Predictor](https://islamabad-houses-price-predictor.streamlit.app/)**

## What the app does

- Lets you choose from the location categories available to the trained model.
- Accepts property area in marla, bedrooms, and bathrooms.
- Uses the saved model in `model.pkl` to estimate a price in Pakistani rupees
  (PKR).
- Maps the model's `other` location category to less-common locations.
- Displays the submitted property details alongside the estimate.

The result is a model estimate based on the project's scraped and processed
property data. It is not a formal valuation, current market quote, or guarantee
of a sale price.

## Repository contents

| File | Description |
| --- | --- |
| `app.py` | Streamlit UI, model loading, input preparation, and price prediction |
| `model.pkl` | Trained scikit-learn decision-tree model used by the app |
| `Zameen.com Islamabad Scraped Data - Sheet1.csv` | Scraped property listings used for the project |
| `Zameen_com_Islamabad_Properties_Data_Science_Project.ipynb` | Notebook with data exploration, preparation, and model training |
| `requirements.txt` | Python dependencies for running the app |
| `APP_WALKTHROUGH.md` | End-to-end explanation and post-ready project brief for `app.py` |

## Run locally

Use Python 3.10 or newer. From the project directory:

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies and start Streamlit:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit prints a local URL in the terminal, typically
`http://localhost:8501`. Keep `model.pkl` in the same project directory as
`app.py`.

## How an estimate is produced

1. The app loads and caches `model.pkl` and checks that the model has the
   expected property and fallback-location features.
2. Location choices are generated from the location feature names stored in
   the model, rather than hard-coded separately in the UI.
3. When the form is submitted, the app constructs a one-row pandas DataFrame
   using the model's exact feature names and order.
4. It fills in area, bedrooms, bathrooms, and the selected location indicator,
   then calls the model's `predict` method.
5. The app displays a formatted PKR estimate, after checking that the returned
   value is finite.

The checked-in model was serialized with scikit-learn 1.9.1. The
`requirements.txt` file pins that version so the model is loaded with the
matching library release.

## Data and model notes

The accompanying notebook documents analysis and training on scraped
Islamabad property listings. As with any estimate trained on historical
listings, predictions may be affected by data quality, missing or uncommon
locations, changes in the market, and property details not included in the
model. Use the estimate as an informational starting point, not as financial
or real-estate advice.

## Project walkthrough

For a detailed, section-by-section explanation of the Streamlit application
and a concise brief suitable for drafting a project post with AI, see
[`APP_WALKTHROUGH.md`](./APP_WALKTHROUGH.md).
