# Islamabad House Price Prediction

A Streamlit app for estimating Islamabad property prices with the project's
trained decision-tree model.

## Run the app

Use Python 3.10 or newer:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Keep `model.pkl` in the project root alongside `app.py`. The app accepts a
property's area in marla, bedrooms, bathrooms, and a location represented in
the trained model. Locations not represented as their own model feature use
the model's `other` category.

The saved model was serialized with scikit-learn 1.9.1; the requirements pin
that version to keep loading and predictions consistent.

Estimates are for informational purposes only and are not formal property
valuations.