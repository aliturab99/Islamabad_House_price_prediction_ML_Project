import html
import math
import pickle
from pathlib import Path

import pandas as pd
import streamlit as st


MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"


@st.cache_resource
def load_model():
    with MODEL_PATH.open("rb") as model_file:
        model = pickle.load(model_file)

    feature_names = getattr(model, "feature_names_in_", None)
    if feature_names is None:
        raise ValueError("The model does not include its expected feature names.")

    required_features = {"area_marla", "beds", "baths"}
    missing_features = required_features.difference(feature_names)
    if missing_features:
        raise ValueError(
            "The model is missing required features: "
            + ", ".join(sorted(missing_features))
        )
    if "location_other" not in feature_names:
        raise ValueError("The model does not include the fallback location feature.")

    return model


st.set_page_config(
    page_title="Islamabad Home Value",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Colour palette
#   Background   #F4F7F5  soft neutral with a faint green tint
#   Surface      #FFFFFF  cards / form
#   Border       #D9E3DD
#   Text         #14231B  headings / body
#   Muted text   #5A6B62  captions / secondary
#   Primary      #1B6B4A  buttons, eyebrow, accents
#   Primary dark #134D35  hover, result card
st.markdown(
    """
    <style>
    :root {
        color-scheme: light;
        --bg: #f4f7f5;
        --surface: #ffffff;
        --border: #d9e3dd;
        --text: #14231b;
        --muted: #5a6b62;
        --primary: #1b6b4a;
        --primary-dark: #134d35;
        --tint: #e7f2ec;
    }

    /* ---------- Base ---------- */
    .stApp {
        background:
            radial-gradient(ellipse at 90% -5%, rgba(27, 107, 74, 0.10), transparent 40%),
            var(--bg);
        color: var(--text);
    }
    header[data-testid="stHeader"] { background: transparent; }
    .block-container {
        max-width: 1120px;
        padding-top: 2.3rem;
        padding-bottom: 3rem;
    }

    /* Force readable text everywhere, regardless of the viewer's theme */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4,
    .stApp p, .stApp li, .stApp strong,
    .stApp label, .stApp label p,
    div[data-testid="stWidgetLabel"] p {
        color: var(--text);
    }
    div[data-testid="stCaptionContainer"],
    div[data-testid="stCaptionContainer"] p,
    div[data-testid="stTooltipIcon"] {
        color: var(--muted);
    }

    /* ---------- Hero ---------- */
    .eyebrow {
        color: var(--primary);
        font-size: 0.76rem;
        font-weight: 750;
        letter-spacing: 0.13em;
        text-transform: uppercase;
    }
    .hero-title {
        color: var(--text) !important;
        font-size: clamp(2.3rem, 5vw, 3.5rem);
        font-weight: 760;
        letter-spacing: -0.055em;
        line-height: 1.05;
        margin: 0.55rem 0 0.8rem;
    }
    .hero-copy {
        color: var(--muted) !important;
        font-size: 1.06rem;
        line-height: 1.65;
        max-width: 650px;
    }

    /* ---------- Form card ---------- */
    div[data-testid="stForm"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1.35rem 1.4rem 1.1rem;
        box-shadow: 0 10px 30px rgba(20, 35, 27, 0.06);
    }

    /* ---------- Inputs ---------- */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"],
    div[data-baseweb="base-input"] {
        background: #f9fbfa !important;
        border-color: var(--border) !important;
        color: var(--text) !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div,
    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input {
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
    }
    div[data-baseweb="select"] svg { fill: var(--muted); }
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="base-input"]:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(27, 107, 74, 0.18) !important;
    }
    div[data-testid="stNumberInput"] button {
        background: var(--tint) !important;
        color: var(--primary-dark) !important;
        border-color: var(--border) !important;
    }
    div[data-testid="stNumberInput"] button:hover {
        background: #d5e9de !important;
    }

    /* Dropdown list */
    div[data-baseweb="popover"] ul[role="listbox"],
    div[data-baseweb="popover"] div[data-baseweb="menu"] {
        background: var(--surface) !important;
    }
    div[data-baseweb="popover"] li { color: var(--text) !important; }
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="popover"] li[aria-selected="true"] {
        background: var(--tint) !important;
    }

    /* ---------- Button ---------- */
    .stButton > button[kind="primaryFormSubmit"],
    button[data-testid="stBaseButton-primaryFormSubmit"] {
        background: var(--primary) !important;
        border: 0 !important;
        border-radius: 10px;
        min-height: 2.9rem;
        font-weight: 650;
        color: #ffffff !important;
    }
    .stButton > button[kind="primaryFormSubmit"] p,
    button[data-testid="stBaseButton-primaryFormSubmit"] p {
        color: #ffffff !important;
    }
    .stButton > button[kind="primaryFormSubmit"]:hover,
    button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
        background: var(--primary-dark) !important;
    }

    /* ---------- Info box ---------- */
    div[data-testid="stAlert"] {
        background: var(--tint);
        border: 1px solid #c8e0d2;
        border-radius: 14px;
    }
    div[data-testid="stAlert"] p { color: #234536; }
    div[data-testid="stAlert"] svg { fill: var(--primary); }

    /* ---------- Result card ---------- */
    .result-card {
        background: linear-gradient(135deg, #134d35 0%, #1b6b4a 100%);
        border-radius: 18px;
        padding: 1.5rem 1.7rem;
        margin-top: 1.25rem;
        box-shadow: 0 14px 34px rgba(19, 77, 53, 0.25);
    }
    .result-label {
        color: #a9e2c5 !important;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    .result-value {
        color: #ffffff !important;
        font-size: clamp(2rem, 4vw, 2.8rem);
        font-weight: 760;
        letter-spacing: -0.04em;
        margin: 0.35rem 0;
    }
    .result-detail {
        color: #d3ebdd !important;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="eyebrow">Islamabad · Property estimator</div>', unsafe_allow_html=True)
st.markdown(
    '<h1 class="hero-title">Find your home’s estimated value.</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="hero-copy">Explore an instant price estimate based on property '
    'size, rooms, and location in Islamabad.</p>',
    unsafe_allow_html=True,
)

try:
    model = load_model()
except (
    AttributeError,
    EOFError,
    FileNotFoundError,
    ImportError,
    ModuleNotFoundError,
    pickle.UnpicklingError,
    ValueError,
) as error:
    st.error(f"Could not load the house-price model: {error}")
    st.stop()

feature_names = list(model.feature_names_in_)
location_features = [
    name.removeprefix("location_")
    for name in feature_names
    if name.startswith("location_")
]
location_options = sorted(
    (location for location in location_features if location != "other"),
    key=str.casefold,
)
location_options.append("other")

input_column, guide_column = st.columns([1.35, 0.85], gap="large")
with input_column:
    st.subheader("Property details")
    st.caption("Enter the basics to get a model-based estimate.")

    with st.form("property_estimate"):
        location = st.selectbox(
            "Islamabad location",
            options=location_options,
            format_func=lambda value: (
                "Other / less common location" if value == "other" else value
            ),
        )
        area_marla = st.number_input(
            "Property area (marla)",
            min_value=0.5,
            max_value=500.0,
            value=10.0,
            step=0.5,
            help="One kanal is 20 marla.",
        )
        beds_column, baths_column = st.columns(2)
        with beds_column:
            beds = st.number_input("Bedrooms", min_value=1, max_value=20, value=4)
        with baths_column:
            baths = st.number_input("Bathrooms", min_value=1, max_value=20, value=4)
        submitted = st.form_submit_button(
            "Estimate property value",
            type="primary",
            use_container_width=True,
        )

with guide_column:
    st.subheader("A quick guide")
    st.markdown(
        """
        **01 · Choose a location**

        Select a location used by the trained model. Less common areas are grouped
        under “Other”.

        **02 · Add property details**

        Enter the size in marla along with bedroom and bathroom counts.

        **03 · Get an estimate**

        The saved decision-tree model returns an estimated price in Pakistani rupees.
        """
    )
    st.info(
        "This estimate is for information only. It is not a formal valuation or "
        "a guarantee of a sale price."
    )

if submitted:
    model_input = pd.DataFrame(0.0, index=[0], columns=feature_names)
    model_input.loc[0, "area_marla"] = area_marla
    model_input.loc[0, "beds"] = beds
    model_input.loc[0, "baths"] = baths

    location_feature = f"location_{location}"
    if location_feature not in model_input.columns:
        location_feature = "location_other"
    model_input.loc[0, location_feature] = 1.0

    prediction = float(model.predict(model_input)[0])
    if not math.isfinite(prediction):
        st.error("The model returned an invalid estimate. Please try different inputs.")
    else:
        location_label = (
            "Other / less common location" if location == "other" else location
        )
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">Estimated property value</div>
                <div class="result-value">PKR {prediction:,.0f}</div>
                <div class="result-detail">
                    {html.escape(location_label)} · {area_marla:g} marla ·
                    {beds} bedrooms · {baths} bathrooms
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )