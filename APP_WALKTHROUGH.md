# `app.py` — End-to-End Walkthrough

This note explains the Streamlit application from startup through prediction.
It can also be used as background material when drafting a project post.

## At a glance

The app is a small interface around a trained scikit-learn
`DecisionTreeRegressor`. A user selects an Islamabad location and enters the
property's area, bedrooms, and bathrooms. The app arranges those values in the
feature layout expected by `model.pkl`, asks the model for a prediction, and
shows the estimated price in PKR.

The application uses the model that is already saved in the repository. It
does not train or update the model when a user submits the form.

## End-to-end flow

### 1. Imports and model location

The file imports:

- `streamlit` for the web UI.
- `pandas` to create the correctly shaped model input.
- `pickle` and `Path` to load `model.pkl` beside `app.py`.
- `math` to reject a non-finite prediction.
- `html` to safely escape the user-facing location text before rendering it
  inside custom HTML.

Resolving the model path relative to `__file__` means the app can locate the
pickle regardless of the shell's current working directory, as long as the
model file remains beside the Python file.

### 2. Loading and checking the model

`load_model()` is decorated with `st.cache_resource`, so Streamlit can reuse the
loaded model between reruns rather than unpickling it for every interaction.
After loading, it checks that:

- the model exposes its trained feature names;
- the numeric features `area_marla`, `beds`, and `baths` are present; and
- the fallback feature `location_other` is present.

These checks make a mismatched or incomplete model fail with an explicit error
instead of silently producing an incorrectly shaped prediction. The app shows
a visible error if loading fails. Because pickle files can execute code when
loaded, only use a model file from a trusted source.

### 3. Page setup and visual design

`st.set_page_config()` sets the browser title, home icon, wide layout, and
collapsed sidebar. The CSS passed to `st.markdown()` defines the interface's
light neutral background, green accent palette, centered content width, form
controls, button, information box, and dark-green result card.

The hero heading and introductory copy identify the app as an Islamabad
property estimator. Custom HTML is used for some display elements; the dynamic
location shown in the result is escaped with `html.escape()` before inclusion.

### 4. Location choices from model features

The app reads `model.feature_names_in_` and extracts feature names prefixed
with `location_`. This keeps the dropdown aligned with the categories encoded
when the model was trained, rather than maintaining a separate list that might
drift out of sync.

The location named `other` is presented with the friendlier label
“Other / less common location” and is placed last in the dropdown. It is the
fallback category the model learned for locations that were grouped together
during training.

### 5. The property form

The page uses two columns: the property form and a short usage guide with a
valuation disclaimer. The form collects:

| Input | Control | Accepted values / default |
| --- | --- | --- |
| Islamabad location | Select box | Categories available in the saved model |
| Area | Number input | 0.5–500 marla, default 10; one kanal is 20 marla |
| Bedrooms | Number input | 1–20, default 4 |
| Bathrooms | Number input | 1–20, default 4 |

The user submits all fields with the “Estimate property value” form button.

### 6. Preparing the model input

On submission, the app creates a one-row DataFrame with every column from
`model.feature_names_in_`, initialized to zero. It then fills in the three
numeric property features and sets the selected location's one-hot feature to
one.

Using the model's stored feature names and their order is important: the
training process encoded locations as individual features, so a prediction
must have the same columns in the same order. If a selected location feature
is missing, the app selects `location_other` instead.

### 7. Prediction and display

The app calls `model.predict()` with the prepared DataFrame and converts the
first result to a Python float. It checks `math.isfinite()` before displaying
the value; an invalid numeric result produces a visible error.

For a valid prediction, a styled result card shows:

- the estimated price formatted as `PKR` with thousands separators;
- the location; and
- area, bedrooms, and bathrooms entered by the user.

The displayed estimate is explicitly described in the app as informational
only, not a formal valuation or a guaranteed sale price.

## Important implementation details

- **Model and UI stay in sync:** location options and input column order come
  from the saved estimator's feature names.
- **Fast reruns:** `st.cache_resource` caches the deserialized estimator.
- **Visible errors:** model loading and validation failures are shown in the
  page rather than hidden behind a guessed fallback.
- **Safer result rendering:** dynamic location text is HTML-escaped.
- **Input scope:** the model uses location, area, bedrooms, and bathrooms; the
  app does not account for other factors such as condition, age, finishes, or
  exact plot dimensions.
- **Model compatibility:** `requirements.txt` pins scikit-learn to 1.9.1, the
  version used to serialize the checked-in estimator.

## Post-ready project summary

> I built a Streamlit app that turns a trained Islamabad house-price model into
> an interactive property estimator. Users select a location and enter area in
> marla, bedrooms, and bathrooms to receive an estimated price in PKR. The app
> loads the saved scikit-learn model, derives its location options and feature
> layout directly from the trained model, and handles less-common locations
> through the model's `other` category. The project includes a data-science
> notebook, scraped property listings, and a deployed web app. Estimates are
> for information only and are not formal valuations.
>
> **Try it:** https://islamabad-houses-price-predictor.streamlit.app/

## Suggested post outline

1. Introduce the goal: make Islamabad property-price exploration accessible.
2. Explain the inputs and the instant PKR estimate.
3. Mention that the UI is powered by a saved decision-tree model and a
   Streamlit form.
4. Highlight the model-driven location dropdown and fallback category.
5. Share the live app link and invite readers to try it.
6. Note that predictions are informational and not formal property valuations.
