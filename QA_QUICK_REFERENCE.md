# QA Analysis - Quick Reference Card

**Version**: 2.0 | **Updated**: November 2, 2025

---

## Quick Commands

### Run Full Analysis
```bash
cd /Users/venkatapagadala/Desktop/telecom_app
source venv/bin/activate
python3 qa_multidirectional.py
```

### Run Clustering Analysis
```bash
python3 qa_clustering.py
```

### View Reports
```bash
# Multi-directional report
cat qa_multidirectional_report.json | python3 -m json.tool | less

# Clustering report
cat qa_analysis_report.json | python3 -m json.tool | less
```

---

## What Each Analysis Does

### Multi-Directional QA (`qa_multidirectional.py`)
**Tests**: 50 diverse queries from 4 directions
**Output**: Hierarchy validation, rollup/drilldown testing, recommendations

**Directions**:
1. Bottom-to-Top: Query → L5 → L4 → L3 → L2 → L1
2. Top-to-Bottom: L1 → L2 → L3 → L4 → L5
3. Middle-to-Top: L3 → L2 → L1
4. Middle-to-Bottom: L3 → L4 → L5

**When to Use**: After updating decision tree, monthly quality checks

### Clustering Analysis (`qa_clustering.py`)
**Tests**: All classified queries from results folder
**Output**: Quality metrics, cluster analysis, issue detection

**Metrics**: Purity, confidence, variance, feedback score
**Flags**: LOW_CONFIDENCE, LOW_PURITY, HIGH_VARIANCE

**When to Use**: Daily/weekly quality monitoring, pattern detection

---

## Current System Status

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Classification Rate | 94.0% | 98%+ | 🟡 |
| Hierarchy Validity | 100% | 100% | ✅ |
| Rollup Validity | 100% | 100% | ✅ |
| Drilldown Validity | 76.6% | 90%+ | 🟡 |
| Avg Confidence | 5.05 | 30+ | 🔴 |
| Low Confidence % | 66% | <20% | 🔴 |

---

## Critical Issues to Fix

### 1. Unclassified Queries (3)
```
galaxy watch 6 classic
galaxy buds pro 3
galaxy s25 rumors
```
**Fix**: Add keywords to [telecom-classification.json](telecom-classification.json)

### 2. Low Confidence (31 queries)
**Top Issues**:
- Samsung devices (0.7-1.0 confidence)
- Google Pixel (0.7 confidence)
- Generic support (0.2-0.9 confidence)

**Fix**: Expand keyword coverage

### 3. Drilldown Failures (11 queries)
**Common Pattern**: Generic topics don't match specific actions
**Fix**: Add granular topics for support actions

---

## Quick Fixes

### Add Missing Samsung Keywords
```json
{
  "L2_wearables": {
    "name": "Samsung Wearables",
    "keywords": ["galaxy watch", "watch 6", "watch classic"]
  },
  "L2_accessories": {
    "name": "Accessories - Audio",
    "keywords": ["galaxy buds", "buds pro"]
  }
}
```

### Add Support Action Topics
```json
{
  "L4_activate": {
    "topic": "Phone Activation",
    "keywords": ["activate", "activation", "activate new phone"]
  },
  "L4_unlock": {
    "topic": "Device Unlocking",
    "keywords": ["unlock", "unlock phone", "unlock device"]
  }
}
```

---

## Reading the Output

### Multi-Directional Analysis

**✅ = Passed validation**
```
✅ [1] buy iphone 17 pro max | Conf: 18.9
```

**❌ = Failed validation or unclassified**
```
❌ [14] galaxy watch 6 classic | UNCLASSIFIED
❌ [43] Transactional → Prepaid Plan Purchase | Conf: 0.9
```

### Recommendations

**🔴 CRITICAL** = Must fix (affects classification rate)
**🟡 HIGH** = Should fix (affects confidence)
**🟢 MEDIUM** = Nice to fix (affects drilldown)

---

## Interpreting Metrics

### Confidence Scores
- **0-5**: Very weak (generic fallback)
- **5-10**: Weak (partial match)
- **10-15**: Moderate (good match)
- **15-20**: Good (strong match)
- **20+**: Excellent (exact match)

### Validation Percentages
- **100%**: Perfect (hierarchy, rollup)
- **90%+**: Good (target for drilldown)
- **80-90%**: Acceptable
- **<80%**: Needs improvement

### Classification Rate
- **98%+**: Excellent coverage
- **94-98%**: Good (current)
- **90-94%**: Acceptable
- **<90%**: Poor coverage

---

## Workflow

### After Updating Decision Tree

1. **Run Multi-Directional Analysis**
   ```bash
   python3 qa_multidirectional.py
   ```

2. **Check Recommendations**
   - Look for CRITICAL issues first
   - Note unclassified queries
   - Review drilldown failures

3. **Fix Issues**
   - Add missing keywords
   - Expand low-confidence topics
   - Create granular action topics

4. **Re-run Analysis**
   ```bash
   python3 qa_multidirectional.py
   ```

5. **Compare Metrics**
   - Classification rate improved?
   - Confidence increased?
   - Drilldown validity better?

### Weekly Quality Check

1. **Run Clustering Analysis**
   ```bash
   python3 qa_clustering.py
   ```

2. **Review Cluster Issues**
   - LOW_CONFIDENCE clusters
   - LOW_PURITY clusters
   - HIGH_VARIANCE clusters

3. **Export Report**
   ```bash
   cat qa_analysis_report.json
   ```

4. **Track Trends**
   - Avg confidence over time
   - Classification rate changes
   - New issue patterns

---

## Files Reference

### Analysis Scripts
- `qa_multidirectional.py` - Multi-directional testing
- `qa_clustering.py` - Cluster quality analysis

### Reports (Auto-generated)
- `qa_multidirectional_report.json` - 4-directional results
- `qa_analysis_report.json` - Clustering results

### Documentation
- `QA_MULTIDIRECTIONAL_SUMMARY.md` - Comprehensive guide (15KB)
- `QA_MULTIDIRECTIONAL_UPDATE.md` - Update summary (this version)
- `QA_CLUSTERING_IMPLEMENTATION.md` - Clustering guide (52KB)
- `QA_QUICK_START.md` - Quick start (17KB)
- `QA_CLUSTERING_SUMMARY.md` - Clustering overview (17KB)
- `QA_QUICK_REFERENCE.md` - This file

### Configuration
- `telecom-classification.json` - Decision tree (edit here)
- `telecom_classifier.py` - Classification engine

---

## Common Tasks

### Find Unclassified Queries
```python
import json
with open('qa_multidirectional_report.json', 'r') as f:
    report = json.load(f)
    unclassified = report['detailed_metrics']['classification']['unclassified_queries']
    print('\n'.join(unclassified))
```

### Find Low Confidence Topics
```python
import json
with open('qa_multidirectional_report.json', 'r') as f:
    report = json.load(f)
    low_conf = report['detailed_metrics']['issues']['low_confidence']
    for item in low_conf:
        print(f"{item['query']:40s} → {item['topic']:40s} (conf: {item['confidence']:.2f})")
```

### Count Drilldown Failures by Topic
```python
import json
from collections import Counter

with open('qa_multidirectional_report.json', 'r') as f:
    report = json.load(f)
    failures = report['detailed_metrics']['issues']['drilldown_failures']
    topics = Counter([f['topic'] for f in failures])
    for topic, count in topics.most_common():
        print(f"{topic:40s} {count} failures")
```

---

## Troubleshooting

### Error: "No module named 'telecom_classifier'"
```bash
# Make sure you're in the right directory
cd /Users/venkatapagadala/Desktop/telecom_app
python3 qa_multidirectional.py
```

### Error: "File not found: telecom-classification.json"
```bash
# Check the path in qa_multidirectional.py line 664
# Should be: /Users/venkatapagadala/Desktop/telecom-classification.json
```

### KeyError on classification fields
- Already fixed in v2.0
- Update qa_multidirectional.py if using old version

---

## Success Checklist

After implementing recommendations:

- [ ] Classification rate > 98%
- [ ] Avg confidence > 20
- [ ] Low confidence % < 30%
- [ ] Drilldown validity > 90%
- [ ] All Samsung wearables classified
- [ ] All Samsung accessories classified
- [ ] All support actions validated
- [ ] No unclassified queries

---

## Support

**Issues?** Check the full documentation:
- [QA_MULTIDIRECTIONAL_SUMMARY.md](QA_MULTIDIRECTIONAL_SUMMARY.md) - Detailed analysis
- [QA_MULTIDIRECTIONAL_UPDATE.md](QA_MULTIDIRECTIONAL_UPDATE.md) - Latest updates
- [QA_CLUSTERING_IMPLEMENTATION.md](QA_CLUSTERING_IMPLEMENTATION.md) - Clustering guide

**Questions?** Review the generated reports:
- `qa_multidirectional_report.json` - Full metrics and recommendations
- `qa_analysis_report.json` - Cluster quality issues

---

**Last Updated**: November 2, 2025
**Version**: 2.0
**Status**: Production-Ready ✅
