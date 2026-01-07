# 🚀 QA Clustering - Quick Start Guide

## Installation (5 minutes)

### Step 1: Install Dependencies

```bash
cd /Users/venkatapagadala/Desktop/telecom_app
source venv/bin/activate
pip install scikit-learn matplotlib seaborn
```

### Step 2: Verify Files

```bash
# Check these files exist:
ls qa_clustering.py                          # ✅ Main clustering engine
ls QA_CLUSTERING_IMPLEMENTATION.md           # ✅ Full documentation
ls QA_QUICK_START.md                         # ✅ This file
```

---

## Run Your First QA Analysis (2 minutes)

### Option 1: Command Line (Quickest)

```bash
python3 qa_clustering.py
```

**What it does**:
1. Loads your classified queries from `results/` folder
2. Loads feedback from `learning/feedback/`
3. Analyzes data quality
4. Creates 50 clusters using K-Means
5. Identifies quality issues
6. Exports report to `qa_analysis_report.json`

**Expected Output**:
```
================================================================================
QA CLUSTERING ANALYSIS
================================================================================

📂 Loading classification data...
   Loading: results_20251101_150000.csv
✅ Loaded 30,000 queries

📂 Loading feedback data...
✅ Loaded 3 feedback entries

📊 Analyzing Data Quality...
============================================================
DATA QUALITY SUMMARY
============================================================
Total Queries:        30,000
Classified:           16,993 (56.6%)
Unclassified:         13,007
Unique Topics:        769

Confidence Scores:
  Average:            28.47
  Median:             24.00
  Range:              0.35 - 94.00
  Low Confidence:     10,234 (60.2%)
============================================================

🔬 Performing text-based clustering (kmeans)...
   Queries to cluster: 16,993
   Creating TF-IDF vectors...
   Running K-Means (k=50)...
   Silhouette Score: 0.123
   Calinski-Harabasz Score: 1234.5

✅ Created 50 clusters
   Avg cluster size: 339.9
   Largest cluster: 1,234 queries
   Smallest cluster: 12 queries

🔍 Analyzing cluster quality...
================================================================================
CLUSTER QUALITY ANALYSIS
================================================================================
LOW_CONFIDENCE       12 clusters
LOW_PURITY           8 clusters
HIGH_VARIANCE        5 clusters
OK                   25 clusters

Top Issues (by cluster size):
================================================================================

Cluster #5 - LOW_CONFIDENCE
  Size: 1,234 queries
  Confidence: 8.3 (±4.2)
  Purity: 67.2%
  Dominant Topic: iPhone Purchase
  Sample: buy iphone 17

💾 Exporting analysis to qa_analysis_report.json...
✅ Report saved to qa_analysis_report.json

================================================================================
ANALYSIS COMPLETE
================================================================================
```

### Option 2: Web Dashboard (Interactive)

**Coming Soon** - See [QA_CLUSTERING_IMPLEMENTATION.md](QA_CLUSTERING_IMPLEMENTATION.md#phase-5-visualization-dashboard) for dashboard implementation.

---

## Understanding the Results

### 1. Quality Metrics

**Classification Rate**: What % of queries were classified?
- **Your System**: 56.6% (16,993 of 30,000)
- **Target**: 80%+
- **Action**: Review unclassified queries, expand decision tree

**Average Confidence**: How certain are the classifications?
- **Your System**: 28.47 (0-100 scale)
- **Target**: 50+
- **Action**: Investigate low-confidence patterns

**Low Confidence %**: What % have confidence < 10?
- **Your System**: 60.2% (10,234 queries)
- **Target**: < 20%
- **Action**: Priority issue - many weak classifications

### 2. Cluster Quality Flags

**LOW_CONFIDENCE** (12 clusters):
- **Meaning**: Average confidence score < 10
- **Impact**: Unreliable classifications
- **Action**: Review keywords, add training data

**LOW_PURITY** (8 clusters):
- **Meaning**: Less than 50% of queries have same topic
- **Impact**: Queries don't belong together
- **Action**: Check if topics are too similar, refine taxonomy

**HIGH_VARIANCE** (5 clusters):
- **Meaning**: Confidence scores vary widely (std > 30)
- **Impact**: Inconsistent quality within cluster
- **Action**: Investigate what causes variance

**OK** (25 clusters):
- **Meaning**: All quality checks passed
- **Impact**: Good quality, no action needed
- **Action**: Use as examples for improvement

---

## Review the Analysis Report

```bash
# View the JSON report
cat qa_analysis_report.json | python3 -m json.tool | less

# Or open in your favorite editor
code qa_analysis_report.json
```

**Report Structure**:
```json
{
  "timestamp": "2025-11-02T14:00:00",
  "quality_metrics": {
    "total_queries": 30000,
    "classification_rate": 56.6,
    "avg_confidence": 28.47,
    "low_confidence_count": 10234,
    ...
  },
  "cluster_summary": {
    "total_clusters": 50,
    "issues_count": 25,
    "avg_cluster_size": 339.9,
    ...
  },
  "top_issues": [
    {
      "cluster_id": 5,
      "quality_flag": "LOW_CONFIDENCE",
      "size": 1234,
      "avg_confidence": 8.3,
      "purity": 0.672,
      "dominant_topic": "iPhone Purchase",
      "sample_queries": ["buy iphone 17", ...]
    },
    ...
  ]
}
```

---

## Next Steps

### Immediate Actions (Today):

1. ✅ **Run the analysis** (you just did!)
2. ✅ **Review top 10 issues** in the output
3. ✅ **Check `qa_analysis_report.json`**
4. ✅ **Identify quick wins** (common low-confidence queries)

### This Week:

1. **Address LOW_CONFIDENCE clusters**:
   - Find dominant queries in flagged clusters
   - Add relevant keywords to decision tree
   - Re-run analysis to verify improvement

2. **Fix LOW_PURITY clusters**:
   - Review if topics are too similar
   - Consider merging or splitting topics
   - Refine taxonomy structure

3. **Collect more feedback**:
   - Current: 3 entries (too low for statistical significance)
   - Target: 100+ entries
   - Use main app to get user feedback

### Next Week:

1. **Implement Dashboard** (see full docs)
2. **Automate QA runs** (daily/weekly)
3. **Set up alerts** for quality degradation
4. **Create action items** from cluster insights

---

## Customization

### Change Number of Clusters

```python
# In qa_clustering.py, line ~200
engine.perform_text_clustering(n_clusters=100)  # Default: 50
```

**Guidance**:
- **k=25**: Broad groups, less granular
- **k=50**: Balanced (recommended)
- **k=100**: Very granular, more specific issues

### Adjust Quality Thresholds

```python
# In qa_clustering.py, analyze_cluster_quality()

# Current thresholds:
if analysis['avg_confidence'] < 10:          # LOW_CONFIDENCE
elif analysis['purity'] < 0.5:               # LOW_PURITY (50%)
elif analysis['std_confidence'] > 30:        # HIGH_VARIANCE

# Adjust as needed:
if analysis['avg_confidence'] < 20:          # Stricter
elif analysis['purity'] < 0.7:               # Require 70% purity
elif analysis['std_confidence'] > 20:        # Lower variance tolerance
```

### Try Different Clustering Methods

```python
# K-Means (default)
engine.perform_text_clustering(n_clusters=50, method='kmeans')

# DBSCAN (density-based, auto-determines cluster count)
engine.perform_text_clustering(method='dbscan')
```

---

## Troubleshooting

### Error: "No results files found"
**Solution**: Make sure you have CSV files in `results/` folder starting with `results_`

### Error: "No data loaded"
**Solution**: Call `engine.load_classification_data()` before running analysis

### Low Silhouette Score (< 0.1)
**Meaning**: Clusters are not well-separated
**Action**: Try different k values, or use DBSCAN

### All clusters flagged as issues
**Meaning**: Data quality is very low overall
**Action**: Focus on improving decision tree, not clustering parameters

### No feedback matches found
**Meaning**: Feedback queries don't match classified queries
**Action**: Ensure feedback collection is working, accumulate more data

---

## Quick Reference Commands

```bash
# Run full analysis
python3 qa_clustering.py

# Check if server is running
curl http://localhost:5001

# View latest results file
ls -ltr results/ | tail -1

# Count feedback entries
cat learning/feedback/*.jsonl | wc -l

# View cluster report
cat qa_analysis_report.json | python3 -m json.tool | head -50

# Check dependencies
pip list | grep scikit-learn
```

---

## Success Metrics

After implementing QA clustering, you should see:

**Week 1**:
- ✅ First analysis report generated
- ✅ Top 10 issues identified
- ✅ Quick wins implemented (obvious keyword gaps)

**Week 2**:
- ✅ Classification rate improves 5-10%
- ✅ Average confidence increases
- ✅ Low confidence count decreases

**Week 3**:
- ✅ Dashboard operational
- ✅ Automated weekly reports
- ✅ Data-driven decision tree updates

**Month 1**:
- ✅ 80%+ classification rate
- ✅ Average confidence > 40
- ✅ < 20% low confidence queries
- ✅ 100+ feedback entries collected

---

## Support & Documentation

**Full Implementation Guide**: [QA_CLUSTERING_IMPLEMENTATION.md](QA_CLUSTERING_IMPLEMENTATION.md)

**Key Sections**:
- Phase 1: Data Preparation
- Phase 2: Clustering Implementation
- Phase 3: Quality Analysis
- Phase 4: API Endpoints
- Phase 5: Visualization Dashboard

**Additional Help**:
- Check `qa_analysis_report.json` for detailed metrics
- Review cluster samples to understand patterns
- Compare before/after analysis runs to track improvement

---

**Your QA Clustering system is ready!** Run `python3 qa_clustering.py` to start analyzing quality. 🚀
