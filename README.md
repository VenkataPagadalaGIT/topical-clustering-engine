# Telecom Query Grouping Web App

Beautiful web application to upload query data with metadata and automatically group them by topical clusters using AI classification.

## Features

- 📤 **Upload CSV/Excel files** with queries and metadata (URL, CPC, rankings, etc.)
- 🤖 **Automatic topical grouping** using hierarchical classification
- 📊 **Interactive dashboards** with multiple views
- 🔍 **Filter and search** through your data
- 📥 **Export results** in Excel (with multiple sheets) or CSV
- 🎯 **Preserve all original columns** from your upload

## What You Upload

CSV or Excel file with columns like:
```
Query/Keyword | URL | CPC | Current Ranking | Search Volume | etc.
```

Example:
```csv
Query,URL,CPC,Current Ranking
buy unlimited plan,/plans/unlimited,8.50,3
what is 5g,/learn/5g,1.20,8
iphone 15 price,/devices/iphone,18.50,2
```

## What You Get

Your data **enriched** with topical groupings:
```
Query | URL | CPC | Ranking | Topical Group | L1 | L2 | L3 Intent | Funnel Stage
```

### Output Columns Added:
- **Topical Group** - Specific topic cluster (e.g., "Unlimited Plan Purchase")
- **L1 Category** - Broad category (e.g., "Mobile Plans")
- **L2 Subcategory** - Subcategory (e.g., "Unlimited Plans")
- **L3 Intent** - Search intent (Transactional, Informational, etc.)
- **Funnel Stage** - Marketing funnel position (Awareness, Purchase, etc.)
- **Commercial Score** - Business value (0-100)
- **Confidence Score** - Classification confidence

### Multiple Views:
1. **All Data** - Complete table with filtering
2. **Grouped by Topic** - Collapsible topic clusters
3. **By Category** - Group by L1 categories
4. **By Intent** - Group by search intent

## Installation

### 1. Install Dependencies

```bash
cd /Users/venkatapagadala/Desktop/telecom_app
pip3 install -r requirements.txt
```

### 2. Run the App

```bash
python3 app.py
```

### 3. Open in Browser

```
http://localhost:5000
```

## Usage

### Step 1: Upload Your File

1. Click "Choose File" or drag & drop
2. Upload CSV or Excel with your query data
3. App auto-detects query column (or uses first column)

### Step 2: Review Results

**Summary Cards:**
- Total queries processed
- Classification rate
- Unique topics found
- Classified count

**Interactive Table:**
- Search queries
- Filter by topic or intent
- Sort by any column
- See all original metadata preserved

**Grouped Views:**
- Click topic headers to expand/collapse
- See all queries in each cluster
- View category distribution
- Analyze intent breakdown

### Step 3: Export

**Excel Export (Recommended):**
- Multiple sheets: All Data, Topics Summary, Categories
- Ready for pivot tables
- Formatted and organized

**Grouped CSV:**
- Sorted by L1 > L2 > Topic > Query
- Easy to import anywhere

## File Structure

```
telecom_app/
├── app.py                      # Flask backend
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── sample_queries.csv          # Sample data
├── templates/
│   └── index.html             # Frontend UI
├── uploads/                   # Uploaded files (auto-created)
└── results/                   # Generated results (auto-created)
```

## API Endpoints

### POST /upload
Upload and classify file
- **Input:** multipart/form-data with 'file'
- **Output:** JSON with classification results

### GET /download/<filename>
Download results CSV

### GET /export/<filename>/<format>
Export in different formats
- **Formats:** `excel`, `grouped-csv`

### GET /api/group-details/<filename>/<group_name>
Get all queries for a specific topic group

## Sample Data

Included `sample_queries.csv` has 40 sample queries with:
- Query
- URL
- CPC
- Current Ranking
- Search Volume
- Keyword Difficulty

Try uploading this to see how it works!

## How Classification Works

### Input Query:
```
"buy unlimited data plan"
```

### Processing:
1. Extract features (action words, pricing signals, etc.)
2. Match against 800+ keyword patterns
3. Score by intent and context
4. Assign to hierarchical categories

### Output:
```json
{
  "topical_group": "Unlimited Plan Purchase",
  "L1_category": "Mobile Plans",
  "L2_subcategory": "Unlimited Plans",
  "L3_intent": "Transactional",
  "funnel_stage": "Decision",
  "commercial_score": 90,
  "confidence_score": 15.90
}
```

## Classification Levels

### L1 - Broad Categories (7 total)
- Mobile Plans
- Internet Services
- Devices
- Business Solutions
- Coverage & Network
- Support & Account
- Promotions & Deals

### L2 - Subcategories (12+ total)
- Prepaid Plans
- Unlimited Plans
- 5G Home Internet
- Smartphones
- etc.

### L3 - Search Intent (9 types)
- **Transactional** (85-100 score) - Ready to buy
- **Informational** (15-40 score) - Learning
- **Comparative** (65-80 score) - Evaluating options
- **Local** (80-95 score) - Near me searches
- **Navigational** (40-60 score) - Finding pages
- **Customer Support** (15-35 score) - Help needed
- etc.

### L4 - Topics (400+ total)
Specific topic phrases for content clustering

### L5 - Keywords (800+ total)
Exact search terms and variations

## Use Cases

### 1. SEO Content Strategy
- Group keywords by topic
- Identify content gaps
- Prioritize by commercial score
- Plan content calendar

### 2. PPC Campaign Organization
- Group keywords by intent
- Separate by funnel stage
- Organize ad groups by topic
- Optimize by commercial value

### 3. Content Audit
- See which topics you rank for
- Find underperforming categories
- Identify optimization opportunities

### 4. Competitor Analysis
- Upload competitor keywords
- See their topical focus
- Find gaps in your coverage

## Tips

### Best Practices

1. **Column Names:**
   - Use "Query" or "Keyword" for main column
   - Other columns can be named anything

2. **Data Quality:**
   - Remove empty rows
   - One query per row
   - Include all metadata you want to keep

3. **File Size:**
   - Up to 100 MB supported
   - 10,000+ queries process in seconds
   - 100,000+ queries take 1-2 minutes

4. **Export Format:**
   - Use Excel for analysis (pivot tables, charts)
   - Use Grouped CSV for imports to other tools

### Filtering Tips

- Use search to find specific queries
- Filter by topic to see clusters
- Filter by intent for funnel analysis
- Combine filters for precision

## Troubleshooting

### Upload Issues

**"Could not detect query column"**
- Rename your query column to "Query" or "Keyword"
- Or place queries in the first column

**"Could not read file"**
- Ensure it's CSV or Excel format
- Check file isn't corrupted
- Try saving as new CSV

### Low Classification Rate

**If < 70% classified:**
- Your queries may be outside telecom domain
- Check for very short/generic queries
- Review unclassified queries
- Consider updating decision tree

### Performance

**Slow processing:**
- Large files (50K+ rows) take longer
- Backend processes in chunks
- Wait for completion (progress shown)

## Advanced Features

### Custom Decision Tree

Edit the decision tree to add your own categories:
```bash
# Edit this file
/Users/venkatapagadala/Desktop/telecom-classification.json
```

### Programmatic Access

Use the API directly:
```python
import requests

# Upload file
files = {'file': open('queries.csv', 'rb')}
response = requests.post('http://localhost:5000/upload', files=files)
data = response.json()

# Download results
requests.get(f"http://localhost:5000/download/{data['results_filename']}")
```

### Batch Processing

Process multiple files:
```bash
for file in *.csv; do
    curl -F "file=@$file" http://localhost:5000/upload > "results_$file.json"
done
```

## Technical Details

### Stack
- **Backend:** Flask (Python)
- **Frontend:** Vanilla JavaScript + HTML/CSS
- **Data Processing:** Pandas
- **Classification:** Custom ML classifier (telecom_classifier.py)
- **Export:** openpyxl for Excel

### Performance
- **Memory:** ~100 MB base + file size
- **Speed:** ~1,000 queries/second
- **Max File Size:** 100 MB (configurable)

### Security
- Files auto-deleted after 24 hours
- No data stored permanently
- Local processing only

## Next Steps

1. **Run the demo:**
   ```bash
   python3 app.py
   # Upload sample_queries.csv
   ```

2. **Upload your data:**
   - Prepare CSV with queries + metadata
   - Upload through web interface
   - Review results

3. **Export and use:**
   - Download Excel for analysis
   - Import to Google Sheets
   - Feed to content planning tools

## Screenshots

### Upload Screen
- Drag & drop interface
- File format auto-detection
- Progress indicator

### Results Dashboard
- Summary metrics cards
- Interactive data table
- Multiple view tabs
- Filter and search

### Grouped View
- Collapsible topic clusters
- Query counts per topic
- Metadata preserved
- Quick navigation

### Export Options
- Excel with multiple sheets
- Grouped CSV sorted
- One-click downloads

## Support

- Review sample_queries.csv for format
- Check console for errors
- Ensure decision tree file exists
- Verify Python dependencies installed

---

**Ready to group your queries?**

```bash
cd /Users/venkatapagadala/Desktop/telecom_app
pip3 install -r requirements.txt
python3 app.py
# Open http://localhost:5000
```

Upload sample_queries.csv to see it in action!
