# 📊 How to Access & Review Feedback Data

## ✅ Feedback IS Being Collected!

Your feedback data is being saved successfully. Here's how to access it:

---

## 🌐 Option 1: Web Feedback Viewer (EASY)

**URL**: http://localhost:5001/feedback-viewer

### What You'll See:
- **Total Feedback Count**
- **Thumbs Up Count** 👍
- **Thumbs Down Count** 👎
- **User Approval Percentage**
- **Corrections Submitted**
- **Full feedback table** with all details
- **Corrections table** with user suggestions

### Features:
- Auto-refreshes every 30 seconds
- Export to CSV button
- View all feedback in one place
- Color-coded (Green=Up, Red=Down)

---

## 📂 Option 2: Direct File Access

### Feedback Files:
```bash
# Location
cd /Users/venkatapagadala/Desktop/telecom_app/learning/feedback

# View today's feedback
cat feedback_20251101.jsonl

# Count total feedback
wc -l feedback_*.jsonl
```

### Corrections Files:
```bash
# Location
cd /Users/venkatapagadala/Desktop/telecom_app/learning/corrections

# Open in Excel/Numbers
open corrections_master.csv
```

---

## 📥 Option 3: Download as Excel

### Method A: Via API
```bash
# Download feedback as Excel
curl -o feedback.xlsx http://localhost:5001/api/export-feedback-excel

# Then open
open feedback.xlsx
```

### Method B: Via Web UI
1. Go to http://localhost:5001/feedback-viewer
2. Click "Export CSV" button
3. File downloads automatically

---

## 📊 Current Feedback Data

**Location**: `/Users/venkatapagadala/Desktop/telecom_app/learning/`

### What's Currently Saved:

**feedback_20251101.jsonl:**
```json
{
  "query": "buy iphone 17 air",
  "classification": {
    "L1": "Devices",
    "L2": "Apple iPhone - Air Edition",
    "L3": "Transactional",
    "L4": "iPhone 17 Air Purchase",
    "funnel": "Purchase",
    "score": 92,
    "confidence": 18.92
  },
  "feedback_type": "up",
  "timestamp": "2025-11-01T15:19:41.384Z",
  "filename": "single_query"
}
```

**corrections_master.csv:**
```csv
timestamp,query,original_L1,original_L2,original_L3,original_L4,suggested_correction,filename
2025-11-01T15:20:35.168Z,buy iphone 17 air  vs iphone 17 pro max,Devices,Apple iPhone - Air Edition,Transactional,iPhone 17 Air Purchase,Iphone 17 air vs Iphone 17 pro max,single_query
```

---

## 🎯 Quick Access Commands

### View All Feedback:
```bash
cat /Users/venkatapagadala/Desktop/telecom_app/learning/feedback/*.jsonl
```

### Count Thumbs Up:
```bash
grep '"feedback_type": "up"' /Users/venkatapagadala/Desktop/telecom_app/learning/feedback/*.jsonl | wc -l
```

### Count Thumbs Down:
```bash
grep '"feedback_type": "down"' /Users/venkatapagadala/Desktop/telecom_app/learning/feedback/*.jsonl | wc -l
```

### Open Corrections in Excel:
```bash
open /Users/venkatapagadala/Desktop/telecom_app/learning/corrections/corrections_master.csv
```

---

## 🔄 Convert JSONL to Excel (Manual)

If you want to convert feedback JSONL to Excel manually:

```python
import pandas as pd
import json

# Read JSONL
feedback = []
with open('learning/feedback/feedback_20251101.jsonl', 'r') as f:
    for line in f:
        feedback.append(json.loads(line))

# Convert to DataFrame
df = pd.DataFrame(feedback)

# Flatten nested classification
df['L1'] = df['classification'].apply(lambda x: x['L1'])
df['L2'] = df['classification'].apply(lambda x: x['L2'])
df['L3'] = df['classification'].apply(lambda x: x['L3'])
df['L4'] = df['classification'].apply(lambda x: x['L4'])
df['confidence'] = df['classification'].apply(lambda x: x['confidence'])

# Save to Excel
df.to_excel('feedback_export.xlsx', index=False)
```

---

## 📋 Sample Data Updated!

### NEW: 100 Keywords

**File**: `/Users/venkatapagadala/Desktop/telecom_app/static/sample_queries_100.csv`

**Includes**:
- iPhone models (17, 16, 15, 14, 13, 12, 11, SE, etc.)
- Samsung Galaxy (S24, S25, A54, Z Fold, etc.)
- Google Pixel (9 Pro, 9, 8)
- Mobile plans (unlimited, family, prepaid)
- Internet services (5G home, fiber)
- Support queries

**To Use**:
1. Go to http://localhost:5001
2. Click "Try Sample Data" tab
3. Click "Load Sample Dataset"
4. See 100 queries classified!

---

## 🎨 Feedback Viewer Features

### Dashboard View:
```
┌─────────────────────────────────────────────────────────┐
│  Total Feedback: 2  │  Thumbs Up: 1  │  Thumbs Down: 1  │
│  Accuracy: 50%      │  Corrections: 1                   │
└─────────────────────────────────────────────────────────┘
```

### Feedback Table:
| Time | Query | Classification | Feedback | Confidence |
|------|-------|---------------|----------|------------|
| 3:19 PM | buy iphone 17 air | iPhone 17 Air Purchase | 👍 Correct | 18.92 |
| 3:19 PM | buy iphone 17 air vs... | iPhone 17 Air Purchase | 👎 Wrong | 18.92 |

### Corrections Table:
| Time | Query | Original | Suggested Correction |
|------|-------|----------|---------------------|
| 3:20 PM | buy iphone 17 air vs... | iPhone 17 Air Purchase | iPhone 17 air vs iPhone 17 pro max |

---

## 🔧 Troubleshooting

### "No feedback data"
→ Give some feedback first! Click 👍 or 👎 on any classification

### "File not found"
→ Feedback files are created when you give first feedback

### "Can't open CSV"
→ Try: `open -a "Microsoft Excel" corrections_master.csv`

---

## 📊 Analytics You Can Do

### Calculate Accuracy:
```bash
total=$(grep -c '"feedback_type"' learning/feedback/*.jsonl)
thumbs_up=$(grep -c '"feedback_type": "up"' learning/feedback/*.jsonl)
accuracy=$((thumbs_up * 100 / total))
echo "Accuracy: $accuracy%"
```

### Find Most Corrected Topics:
```bash
cut -d',' -f6 learning/corrections/corrections_master.csv | tail -n +2 | sort | uniq -c | sort -rn
```

### View Feedback by Day:
```bash
ls -lh learning/feedback/
```

---

## 🎉 Summary

✅ **Feedback IS collecting** (2 entries already!)
✅ **Corrections ARE saving** (1 correction recorded!)
✅ **Web viewer available** at http://localhost:5001/feedback-viewer
✅ **Excel export works** via API endpoint
✅ **Sample data upgraded** to 100 keywords
✅ **Files accessible** in `/learning/` folder

**Everything is working!** 🚀

---

## 🆕 What's New

1. ✅ **Feedback Viewer Page** - Pretty dashboard at `/feedback-viewer`
2. ✅ **Excel Export API** - Download feedback as `.xlsx`
3. ✅ **100 Keyword Sample** - Upgraded from 40 to 100 queries
4. ✅ **Auto-refresh** - Viewer updates every 30 seconds
5. ✅ **Color-coded tables** - Green for 👍, Red for 👎

---

**To view feedback RIGHT NOW:**
```bash
open http://localhost:5001/feedback-viewer
```

Or manually:
```bash
open /Users/venkatapagadala/Desktop/telecom_app/learning/corrections/corrections_master.csv
```
