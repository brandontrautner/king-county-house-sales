# King County House Sales

A data analytics project examining 21,000+ residential home sales in King County, WA (Seattle metropolitan area). Built a clean analytical layer from raw Kaggle sales data enriched with USPS zip code reference data, using PostgreSQL, Python, and Tableau to answer three core questions: Where are property values highest? How do prices trend across market segments? And how does construction grade influence price?

**Live dashboard:** [View on Tableau Public](https://public.tableau.com/app/profile/brandon.trautner/viz/KingCountyHouseSalesAnalysis_17748082547560/OverviewDashboard)

---

## Key Findings

- **Grade is the strongest price predictor.** A clear positive correlation exists between construction grade and price across all market segments, with the most dramatic effect in the luxury tier.
- **Extreme geographic price variation.** Average sale prices range from $234K in Auburn to $2.16M in Bellevue, nearly a 10x difference across the county.
- **Market segments are clearly defined.** The four price tiers show distinct, stable price bands throughout the observation period with minimal overlap.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| PostgreSQL | Relational database and analytical layer |
| pgAdmin | Database management and query interface |
| Python (pandas, SQLAlchemy, psycopg2) | Data ingestion from CSV/Excel to Postgres |
| Tableau Public | Interactive dashboard and visualizations |

---

## Data Sources

**[House Sales in King County, USA](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction)**
21,613 home sales in King County, Washington from May 2014 to May 2015. Includes price, physical features, condition, grade, location coordinates, and zip code.

**[USPS ZIP Code Reference Data](https://postalpro.usps.com/ZIP_Locale_Detail)**
Maps zip codes to city names. Filtered using Python to the 70 King County zip codes present in the sales data and loaded as a lookup table.

---

## Data Pipeline

```
Kaggle CSV + USPS Excel -> Python ingest -> PostgreSQL views -> Tableau dashboard
```

1. **Download.** Single CSV from Kaggle and zip code Excel file from USPS.
2. **Enrich.** USPS zip code data filtered to King County zip codes and loaded as a lookup table.
3. **Ingest.** Python/pandas script loads CSV/Excel into Postgres.
4. **Model.** SQL views built on top of raw tables to create a clean analytical layer.
5. **Visualize.** Master view exported as CSV and loaded into Tableau Public.

---

## Data Modeling Decisions

**Property age at time of sale.** Rather than calculating age relative to today, property age is calculated at the time of each transaction:
```sql
EXTRACT(YEAR FROM TO_TIMESTAMP(date, 'YYYYMMDD"T"HH24MISS')) - yr_built AS property_age
```

**Price segmentation.** Properties are segmented into four tiers for market segment analysis:
```sql
CASE
  WHEN price < 300000  THEN 'entry level'
  WHEN price < 650000  THEN 'mid range'
  WHEN price < 1000000 THEN 'upper mid'
  ELSE 'luxury'
END AS price_segment
```

**Median vs. average price.** Median price is used throughout to avoid skewing results from ultra-luxury outliers, a standard practice in real estate analysis.

**External data enrichment.** The raw Kaggle dataset contained zip codes with no city names. To make the dashboard more accessible to viewers unfamiliar with the Seattle area, USPS zip code data was used to attach city names, joined to the master view via a lookup table.

---

## SQL Views

### `v_orders_complete`
Base view that parses dates and adds calculated columns including price segment, waterfront status, basement status, renovation status, and property age at time of sale.

### `v_monthly_trends`
Monthly average, min, and max price broken down by price segment and waterfront status. Powers the price trend dashboard.

### `v_price_driver_features`
Property-level view adding price per sqft and all feature flags. Used for feature analysis.

### `v_location_analysis`
Zip code level aggregations including average price, price per sqft, average grade, and average condition. One row per zip code ordered by average price descending.

### `v_master_dashboard`
Single denormalized view combining all key fields and city names from the lookup table. Used for Tableau export.

---

## Business Impact

### Grade is the strongest price predictor
King County uses a construction and design quality grade from 1 to 13. The analysis shows a clear positive correlation between grade and price across all market segments. In the luxury segment, grade 10+ properties command significantly higher prices than grade 7 properties. In the entry-level and mid-range segments, most properties fall within grades 6 to 8 and price differences between grades are relatively small.

**Takeaway:** Grade reliably predicts price within each market segment. Buyers in the mid-range segment see little variance between grade 7 and 8 properties, while in the luxury segment, grade 10+ commands a substantial premium.

### Extreme geographic price variation
Average sale prices range from $234K in Auburn (zip 98002) to $2.16M in Bellevue (zip 98039), nearly a 10x difference across King County. The most expensive zip codes cluster around Bellevue and Mercer Island on the eastern shore of Lake Washington. Price per sqft reinforces this: Bellevue averages $568/sqft vs. $151/sqft in Auburn, confirming that location commands a significant premium independent of property size.

### Market segmentation is clearly defined
The four price segments show distinct, stable price bands throughout the observation period with minimal overlap. The luxury segment shows the most month-to-month price volatility, while entry-level through upper-mid segments remain relatively stable, consistent with broader real estate dynamics where luxury is more sensitive to market conditions.

---

## Dashboard Preview

![King County Dashboard](assets/dashboard_preview.png)

---

## Running Locally

### Prerequisites
- PostgreSQL installed and running
- Python 3 with pip
- Tableau Public (free)

### Setup

```bash
# Clone the repo
git clone https://github.com/brandonTraut/king-county-house-sales.git
cd king-county-house-sales

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install pandas sqlalchemy psycopg2-binary
```

### Database setup

```
1. Open pgAdmin
2. Right-click "Databases" -> "Create" -> "Database"
3. Name it: king_county_db
```

### Add data files

Place these files in `data/raw/`:
- `kc_house_data.csv` (Kaggle dataset)
- `zip_codes.xls` (USPS dataset)

### Load data and create views

```bash
# Update PostgreSQL credentials in each script before running

# Load house sales data
python scripts/load_data.py

# Load zip code lookup table
python scripts/load_zip_lookup.py
```

Then run `sql/views.sql` in pgAdmin to create all views.

### Export to Tableau

Run the following query in pgAdmin, export the result as CSV, and load it into Tableau Public:

```sql
SELECT * FROM v_master_dashboard;
```

---

## Future Directions

- **Property size and layout analysis.** Does cost per sqft decrease with larger homes? Is there an optimal bedroom/bathroom ratio per price segment?
- **Renovation and age ROI.** Do renovated properties command a premium over unrenovated properties of similar age and grade?
- **Condition vs. grade analysis.** Are buyers willing to pay more for an older, well-maintained home or a newer, poorly maintained one?
- **Waterfront deep dive.** Quantify the exact price premium waterfront properties command by grade, size, and zip code.
---
Build by: Brandon Trautner | [Tableau Public](https://public.tableau.com/app/profile/brandon.trautner/viz/KingCountyHouseSalesAnalysis_17748082547560/OverviewDashboard)









