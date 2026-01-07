# Excel Classification Report - User Guide

**File**: [classification_report.xlsx](classification_report.xlsx)
**Size**: 17KB
**Worksheets**: 6
**Generated**: November 4, 2025

---

## Quick Start

### Generate Excel Report

```bash
cd /Users/venkatapagadala/Desktop/telecom_app
source venv/bin/activate
python3 export_classifications_excel.py
```

**Output**: `classification_report.xlsx` (17KB)

### Custom File Names

```bash
# Specify custom input/output files
python3 export_classifications_excel.py input_report.json output_file.xlsx
```

---

## Worksheets Overview

### 1. Summary (Overview)

**Contents**:
- Overall metrics (50 queries tested)
- Classification rate: 94.0%
- Average confidence: 5.05
- Validation results (Bottom-to-Top, Middle-to-Top, Middle-to-Bottom)

**Color Coding**:
- 🟢 Green: 100% success rate
- 🟡 Yellow: 80-99% success rate
- 🔴 Red: <80% success rate

**Key Metrics**:
| Metric | Value |
|--------|-------|
| Total Queries | 50 |
| Classified | 47 (94.0%) |
| Avg Confidence | 5.05 |
| Confidence Range | 0.20 - 20.70 |
| Low Confidence | 36 queries |

---

### 2. Bottom-to-Top (Hierarchy Validation)

**Columns**:
- Query ID
- Query text
- L5 Keyword
- L4 Topic
- L3 Intent
- L2 Subcategory
- L1 Category
- Confidence score
- Commercial score
- Validation status (✅/❌)

**Color Coding**:
- **Confidence**:
  - 🟢 Green: ≥15 (good confidence)
  - 🟡 Yellow: 5-14 (moderate confidence)
  - 🔴 Red: <5 (low confidence)

- **Validation**:
  - 🟢 Green: ✅ Valid hierarchy
  - 🔴 Red: ❌ Failed validation or unclassified

**Example Row**:
| ID | Query | L5 | L4 | L3 | L2 | L1 | Conf | Score | Valid |
|----|-------|----|----|----|----|----|----|-------|-------|
| 1 | buy iphone 17 pro max | buy iphone 17 pro max | iPhone 17 Pro Max Purchase | Transactional | Apple iPhone - Pro Series | Devices | 18.92 | 92 | ✅ |

**Total Rows**: 50 queries

---

### 3. Middle-to-Top (Rollup Validation)

**Tests**: Intent → Subcategory → Category mapping

**Columns**:
- Query ID
- Query text
- L3 Intent
- L2 Subcategory
- L1 Category
- Validation status (✅/❌)

**Results**:
- Valid: 47/47 (100%)
- All classified queries show correct rollup

**Intent Types Found**:
- Transactional: 32 queries (68%)
- Comparative: 10 queries (21%)
- Navigational: 2 queries
- Informational: 1 query
- Local: 1 query
- Customer Support: 1 query

---

### 4. Middle-to-Bottom (Drilldown Validation)

**Tests**: Intent → Topic → Keyword → Query matching

**Columns**:
- Query ID
- Query text
- L3 Intent
- L4 Topic
- L5 Keyword
- Confidence score
- Validation status (✅/❌)

**Color Coding**:
- **Confidence**: Same as Bottom-to-Top sheet
- **Validation**:
  - 🟢 Green: ✅ Keywords match query
  - 🔴 Red: ❌ Keywords don't match query

**Results**:
- Valid: 36/47 (76.6%)
- Failed: 11 queries

**Common Failure Pattern**:
- Generic topics (e.g., "Prepaid Plan Purchase") don't match specific actions (e.g., "activate phone")

---

### 5. Recommendations

**Columns**:
- Priority (CRITICAL/HIGH/MEDIUM)
- Category
- Issue description
- Recommended action
- Expected impact

**Color Coding**:
- 🔴 Red: CRITICAL priority
- 🟡 Yellow: HIGH priority
- 🟢 Green: MEDIUM priority

**Current Recommendations**:

#### 🔴 CRITICAL - Coverage
- **Issue**: 3 unclassified queries (6.0%)
- **Queries**: galaxy watch 6 classic, galaxy buds pro 3, galaxy s25 rumors
- **Action**: Add keywords/topics for Samsung wearables, accessories, unreleased devices
- **Impact**: Classification rate 94% → 98%+

#### 🟡 HIGH - Confidence
- **Issue**: 31 queries with confidence < 5 (66%)
- **Action**: Expand keyword coverage for low-confidence topics
- **Impact**: Average confidence 5.05 → 20+

#### 🟢 MEDIUM - Drilldown
- **Issue**: 11 drilldown validation failures
- **Action**: Refine L5 keywords for 'Prepaid Plan Purchase' and similar topics
- **Impact**: Drilldown validity 76.6% → 90%+

---

### 6. Detailed Metrics

**Sections**:

#### Confidence Distribution
| Range | Count | Percentage |
|-------|-------|------------|
| 0-5   | 31    | 66.0%      |
| 5-10  | 5     | 10.6%      |
| 10-15 | 0     | 0%         |
| 15-20 | 10    | 21.3%      |
| 20+   | 1     | 2.1%       |

#### Intent Distribution
| Intent | Count |
|--------|-------|
| Transactional | 32 |
| Comparative | 10 |
| Navigational | 2 |
| Informational | 1 |
| Local | 1 |
| Customer Support | 1 |

#### Category Distribution
| Category | Count |
|----------|-------|
| Devices | 23 |
| Mobile Plans | 10 |
| Internet Services | 8 |
| Support & Account | 6 |

---

## How to Use the Excel Report

### For Executives/Managers

1. **Start with Summary sheet**
   - Get high-level overview
   - Check classification rate (target: 98%+)
   - Review validation success rates

2. **Review Recommendations sheet**
   - Focus on CRITICAL items first
   - Prioritize fixes by impact
   - Plan implementation timeline

3. **Check Detailed Metrics sheet**
   - Understand confidence distribution
   - Review intent patterns
   - Identify trends

### For Data Scientists/Analysts

1. **Analyze Bottom-to-Top sheet**
   - Sort by confidence (lowest first)
   - Identify low-confidence patterns
   - Group by L1/L2 categories
   - Filter unclassified queries

2. **Study Middle-to-Bottom sheet**
   - Filter for failed validations (❌)
   - Analyze drilldown failures by topic
   - Identify keyword gaps

3. **Use Detailed Metrics sheet**
   - Create pivot tables
   - Analyze confidence distribution
   - Compare intent vs. category

### For Content/SEO Teams

1. **Bottom-to-Top sheet**
   - Review commercial scores
   - Identify high-value queries
   - Check category coverage

2. **Recommendations sheet**
   - Implement missing keywords
   - Expand low-confidence topics
   - Prioritize by business impact

---

## Excel Features

### Filtering & Sorting

All data sheets support:
- ✅ Column filtering
- ✅ Multi-level sorting
- ✅ Find & Replace
- ✅ Freeze panes (headers)

### Conditional Formatting

Pre-applied formatting:
- ✅ Color-coded confidence scores
- ✅ Validation status indicators
- ✅ Priority-based recommendation highlighting

### Text Wrapping

- Query columns: Wrapped for readability
- Recommendation columns: Wrapped for full visibility

---

## Common Analysis Tasks

### Find All Unclassified Queries

**Sheet**: Bottom-to-Top

**Steps**:
1. Click on "Valid" column header
2. Filter → Show only ❌
3. Review unclassified queries

**Current Results**: 3 queries
- galaxy watch 6 classic
- galaxy buds pro 3
- galaxy s25 rumors

---

### Find Low Confidence Queries

**Sheet**: Bottom-to-Top

**Steps**:
1. Click on "Confidence" column header
2. Sort → Smallest to Largest
3. Review queries with confidence < 5

**Current Results**: 31 queries (66%)

**Top Low-Confidence Queries**:
- customer service hours (0.20)
- samsung galaxy s24 ultra (0.70)
- pixel 9 pro camera (0.70)
- pixel watch 3 (0.70)
- pixel buds pro 2 (0.70)

---

### Analyze Drilldown Failures

**Sheet**: Middle-to-Bottom

**Steps**:
1. Filter "Valid" column → Show only ❌
2. Group by "L4 Topic"
3. Identify most common failure patterns

**Current Results**: 11 failures

**Common Topics with Failures**:
- Prepaid Plan Purchase: 5 failures
- iPhone Trade-In: 1 failure
- iPhone 17 Pro Max Store Locations: 1 failure
- Others: 4 failures

---

### Create Summary Dashboard

**Using Pivot Tables**:

1. **Confidence by Intent**:
   - Data: Bottom-to-Top sheet
   - Rows: L3 Intent
   - Values: Average of Confidence
   - Result: See which intents have lowest confidence

2. **Validation Rate by Category**:
   - Data: Middle-to-Bottom sheet
   - Rows: L3 Intent
   - Values: Count of Valid (✅)
   - Result: Drilldown success by intent type

3. **Query Distribution**:
   - Data: Detailed Metrics sheet
   - Use pre-calculated distributions
   - Create charts for visualization

---

## Updating the Report

### Re-generate After Changes

1. **Update decision tree** (add keywords/topics)
2. **Re-run QA analysis**:
   ```bash
   python3 qa_multidirectional.py
   ```
3. **Re-create Excel report**:
   ```bash
   python3 export_classifications_excel.py
   ```
4. **Compare before/after** metrics

### Track Improvements

Keep historical copies:
```bash
# Before changes
cp classification_report.xlsx classification_report_v1.xlsx

# After changes
python3 export_classifications_excel.py
mv classification_report.xlsx classification_report_v2.xlsx
```

Compare versions to measure impact.

---

## Troubleshooting

### Error: "File not found: qa_multidirectional_report.json"

**Solution**: Run QA analysis first
```bash
python3 qa_multidirectional.py
```

### Error: "No module named 'openpyxl'"

**Solution**: Install openpyxl
```bash
pip install openpyxl
```

### Excel file won't open

**Causes**:
- File corrupted during generation
- Excel version too old

**Solution**:
- Re-run export script
- Try opening in Google Sheets or LibreOffice
- Update Excel to latest version

---

## File Locations

```
/Users/venkatapagadala/Desktop/telecom_app/
├── export_classifications_excel.py    - Export script
├── classification_report.xlsx          - Generated Excel file
├── qa_multidirectional_report.json   - Source data (JSON)
└── EXCEL_EXPORT_README.md             - This file
```

---

## Integration with Workflow

### Daily Quality Check
```bash
# 1. Run analysis
python3 qa_multidirectional.py

# 2. Generate Excel report
python3 export_classifications_excel.py

# 3. Review in Excel
open classification_report.xlsx

# 4. Implement top 3 recommendations
# 5. Re-run and compare
```

### Weekly Reporting
```bash
# Save dated copy
cp classification_report.xlsx reports/report_$(date +%Y%m%d).xlsx

# Track metrics over time
# Compare classification rates, confidence trends
```

---

## Advanced Features

### Custom Filters

Create named filters for:
- Unclassified queries only
- Low confidence (<5) queries
- Failed drilldown validations
- Specific categories (Devices, Plans, etc.)

### Pivot Tables

Suggested pivots:
1. **Confidence by Category**
2. **Validation Rate by Intent**
3. **Query Count by Topic**
4. **Commercial Score Distribution**

### Charts

Create charts from:
- Confidence distribution (bar chart)
- Intent distribution (pie chart)
- Validation success rates (column chart)
- Trend analysis (line chart over multiple runs)

---

## Summary

The Excel classification report provides:

✅ **6 worksheets** with comprehensive analysis
✅ **Color-coded** metrics for quick visual scanning
✅ **50 queries** tested across 4 directions
✅ **Actionable recommendations** with priorities
✅ **Detailed metrics** for in-depth analysis

**Perfect for**:
- Executive reviews
- Data analysis
- Keyword optimization
- Quality monitoring
- Progress tracking

**Export time**: <5 seconds
**File size**: 17KB
**Compatible with**: Excel 2016+, Google Sheets, LibreOffice

---

**Generated**: November 4, 2025
**Script**: [export_classifications_excel.py](export_classifications_excel.py)
**Source Data**: [qa_multidirectional_report.json](qa_multidirectional_report.json)
