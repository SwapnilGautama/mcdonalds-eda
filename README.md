# 🍟 McDonald's EDA Dashboard

An interactive Streamlit dashboard for exploring McDonald's outlet performance and menu nutrition data — built as part of an IITK EDA assignment.

## 📊 What's Inside

| Page | Contents |
|---|---|
| **Executive Summary** | Top-level KPIs, revenue distribution, ownership split |
| **Outlet Analytics** | Revenue/Profit/GPM deep dive, employee & footfall analysis, Top 10 rankings |
| **Menu & Nutrition** | 75 menu items, 14 categories, nutrient comparisons, Grilled vs Crispy |
| **Geographic Analysis** | World map, India outlet map, US outlet map, revenue by state |
| **KPI Reference Table** | All 78 KPIs with formulas and India/US values, searchable & downloadable |
| **Python Query Bank** | Every analysis query from the notebook, organised by section |

## 🚀 Deploy on Streamlit Community Cloud (Free)

### Step 1 — Push to GitHub

```bash
# Create a new repo on github.com, then:
git init
git add .
git commit -m "Initial commit: McDonald's EDA Dashboard"
git remote add origin https://github.com/YOUR_USERNAME/mcdonalds-eda.git
git push -u origin main
```

### Step 2 — Deploy on Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with your GitHub account
3. Click **"New app"**
4. Set:
   - **Repository**: `YOUR_USERNAME/mcdonalds-eda`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **Deploy**

That's it — Streamlit Cloud will install dependencies from `requirements.txt` and host it for free.

## 🖥 Run Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/mcdonalds-eda.git
cd mcdonalds-eda

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

App opens at `http://localhost:8501`

## 📁 File Structure

```
mcdonalds-eda/
├── app.py              # Main Streamlit application
├── data_loader.py      # All dataset loading functions
├── requirements.txt    # Python dependencies
├── .streamlit/
│   └── config.toml     # Theme configuration (dark McD theme)
└── README.md
```

## 📦 Dependencies

```
streamlit==1.35.0
pandas==2.2.2
numpy==1.26.4
plotly==5.22.0
openpyxl==3.1.2
```

## 📋 Dataset

- **340 outlets** across India (82) and US (258)
- **75 menu items** across 14 categories
- Source: IITK McDonald's EDA Assignment Dataset

## 🎨 Design

Dark theme with McDonald's brand colours (Red `#DA291C` + Gold `#FFC72C`).
Built with Plotly for interactive charts and Streamlit for the UI framework.
