# Adaptive Learning System

## 🧠 How the System Learns and Updates

Your classifier now has **automatic learning capabilities** that allow it to recognize new devices, plans, and patterns, then update the knowledge base automatically.

---

## The Problem You Identified

**Query:** "iPhone 17 Pro Max vs iPhone Air"
**Issue:** This is NOT the same as "iPhone 15 vs Samsung S24"

The old system would try to match this to the closest known pattern (iPhone 15), which is incorrect. The new learning system **automatically detects** and **learns** new device models, then updates the decision tree.

---

## How It Works

### 1. **Pattern Detection**

When a query can't be classified, the learning engine analyzes it for:

#### Device Models
```
iphone 17 pro max     → New iPhone model detected
iphone air            → New iPhone variant detected
samsung galaxy s25    → New Samsung model detected
pixel 9 pro           → New Google Pixel detected
oneplus 12            → New OnePlus model detected
```

#### Plan Types
```
student plan          → New plan category
senior plan           → New plan category
business plan         → New plan type
```

#### Services
```
satellite internet    → New internet type
6g network           → New network technology
mesh wifi            → New connectivity type
```

### 2. **Confidence Scoring**

Each detected pattern gets a confidence score:

```javascript
Confidence Score = Base Detection (30)
                 + Intent Signals (40)
                 + Context Match (30)
```

**High Confidence (≥50):** Automatically added to knowledge base
**Low Confidence (<50):** Flagged for review

### 3. **Automatic Classification**

Based on patterns detected:

```
Query: "iPhone 17 Pro Max price"
├─ Device Detected: "iPhone 17 Pro Max"
├─ Intent: Purchase (keyword: "price")
├─ Confidence: 70
└─ Classification:
   ├─ L1: Devices
   ├─ L2: Smartphones
   ├─ L3: Transactional
   ├─ L4: iPhone 17 Pro Max Purchase
   └─ L5: "iphone 17 pro max price"
```

### 4. **Knowledge Base Update**

**Automatic Process:**
1. Analyze unclassified queries
2. Extract patterns (devices, plans, etc.)
3. Generate high-confidence classifications
4. **Backup** original decision tree
5. **Add** new patterns to tree
6. **Reload** classifier with updated knowledge

---

## Using the Learning Feature

### In the Web App

**After uploading and classifying your data:**

1. Look at the results - you'll see some queries are **Unclassified**
2. Click the **"🧠 Learn & Update Knowledge"** button
3. System analyzes unclassified queries
4. Shows what it learned:
   ```
   ✅ Successfully learned 5 new patterns!

   New Devices: iphone 17 pro max, samsung galaxy s25
   New Plans: student plan
   New Services: satellite internet
   ```
5. Decision tree is **automatically updated**
6. Option to **reclassify** data with new knowledge

### Via API

```bash
curl -X POST http://localhost:5001/api/learn \
  -H "Content-Type: application/json" \
  -d '{"filename": "results_20251101_103000.csv"}'
```

**Response:**
```json
{
  "success": true,
  "added_count": 5,
  "backup_path": "telecom-classification_backup_20251101_103000.json",
  "new_entities": {
    "devices": ["iphone 17 pro max", "samsung galaxy s25"],
    "plans": ["student plan"],
    "services": ["satellite internet"]
  },
  "learning_summary": {
    "new_devices": 2,
    "new_plans": 1,
    "new_services": 1,
    "total_patterns": 4
  }
}
```

---

## Examples

### Example 1: New iPhone Models

**Input Queries:**
```
iPhone 17 Pro Max vs iPhone Air
iPhone 17 price comparison
iPhone Air features
```

**Learning Process:**
1. Detects: "iphone 17 pro max", "iphone air"
2. Creates new topics:
   - "iPhone 17 Pro Max Comparison"
   - "iPhone 17 Pro Max Purchase"
   - "iPhone Air Information"
3. Adds to decision tree under Devices > Smartphones

**Result:**
Next time these queries appear, they're **automatically classified** correctly!

### Example 2: New Plan Types

**Input Queries:**
```
student discount plan unlimited data
senior plan with hotspot
business plan multiple lines
```

**Learning Process:**
1. Detects: "student plan", "senior plan", "business plan"
2. Creates subcategories under Mobile Plans
3. Assigns appropriate intent (Transactional/Informational)

**Result:**
New plan types are now part of the knowledge base!

### Example 3: New Technology

**Input Queries:**
```
6g network speed
satellite internet rural areas
mesh wifi coverage
```

**Learning Process:**
1. Detects new service types
2. Creates topics under Internet Services
3. Classifies based on context

**Result:**
Future queries about these technologies are recognized!

---

## Safety & Backups

### Automatic Backups

**Every time the learning system updates the tree:**
```
Original: telecom-classification.json
Backup:   telecom-classification_backup_20251101_103000.json
```

You can **restore** anytime:
```bash
cp telecom-classification_backup_20251101_103000.json telecom-classification.json
```

### Learning Logs

**Every learning session is logged:**
```
learning/learning_log_20251101_103000.json
```

Contains:
- Timestamp
- Unclassified query count
- All suggestions
- What was added
- Confidence scores

---

## Confidence Levels

### High Confidence (70-100)
**Example:** "iPhone 17 Pro Max price"
- Clear device model detected
- Purchase intent obvious
- **Action:** Add immediately

### Medium Confidence (50-69)
**Example:** "how much is the new iPhone"
- Device implied but not specific
- Intent clear
- **Action:** Add with generic topic

### Low Confidence (<50)
**Example:** "phone upgrade"
- Too vague
- Multiple interpretations
- **Action:** Skip, needs more context

---

## Pattern Recognition

### Device Patterns

```regex
iPhone:  \biphone\s+(\d+|air|ultra|pro|mini|max|plus)
Samsung: \bsamsung\s+(?:galaxy\s+)?([sa]\d+)
Pixel:   \bpixel\s+(\d+)
OnePlus: \boneplus\s+(\d+)
```

### Intent Detection

```
Purchase:     buy, purchase, order, price, cost
Information:  what, how, why, explain, understand
Comparison:   vs, versus, compare, difference
```

### Plan Types

```regex
\b(\w+)\s+plan\b          → Detects: student plan, family plan
\b(\d+)\s*gb\s+data\b     → Detects: 100gb plan, unlimited
```

---

## Best Practices

### 1. Review Before Auto-Update

For production:
```python
# In app.py, increase min_confidence
result = learning_engine.update_decision_tree(suggestions, min_confidence=70)
```

### 2. Periodic Learning

Run learning **after every bulk upload**:
1. Upload your data
2. Review unclassified queries
3. Click "Learn & Update"
4. Reclassify with new knowledge

### 3. Manual Review

Check learning logs:
```bash
cat learning/learning_log_20251101_103000.json
```

Review suggestions before they're added.

### 4. Keep Backups

```bash
# List all backups
ls -lt *_backup_*.json

# Keep monthly backups
cp telecom-classification.json backups/tree_$(date +%Y%m).json
```

---

## Advanced: Custom Patterns

### Add Your Own Detection

Edit `learning_engine.py`:

```python
# Add custom brand
device_patterns = {
    'xiaomi': r'\bxiaomi\s+(\d+)(?:\s+(pro|ultra))*',
    'oppo': r'\boppo\s+(\w+)',
    # Your custom pattern here
}
```

### Adjust Confidence Thresholds

```python
# In analyze_unclassified()
if learned_info.get('device'):
    suggestion['confidence'] += 40  # Increase for device matches
```

---

## Monitoring Learning

### Check What Was Learned

```python
# Via API
GET /api/learning-summary

# Response
{
  "total_sessions": 15,
  "total_patterns_added": 147,
  "top_devices": ["iphone 17", "samsung s25", "pixel 9"],
  "top_plans": ["student plan", "senior plan"],
  "last_learning": "2025-11-01T10:30:00"
}
```

### Learning Statistics

After each session:
- **Added Count:** Number of new patterns
- **New Entities:** Specific devices/plans/services
- **Backup Location:** Where original was saved
- **Confidence Distribution:** How confident the system was

---

## Troubleshooting

### "No patterns found to learn"
**Cause:** All queries are already classified OR patterns are too low-confidence
**Solution:** Review unclassified queries manually, add specific keywords

### "Added count is 0"
**Cause:** Detected patterns but confidence too low
**Solution:** Lower `min_confidence` threshold or improve pattern detection

### "Error updating tree"
**Cause:** Decision tree file permissions or structure issue
**Solution:** Check file exists, is writable, and valid JSON

---

## Future Enhancements

### Planned Features

1. **Manual Approval Mode**
   - Review suggestions before adding
   - Approve/reject each pattern

2. **Confidence Tuning**
   - Adjust thresholds per category
   - Machine learning for better scoring

3. **Merge Suggestions**
   - Combine similar patterns
   - "iPhone 17" + "iPhone 17 Pro" → "iPhone 17 series"

4. **Usage Analytics**
   - Track which learned patterns are used most
   - Remove unused patterns after 6 months

---

## Summary

✅ **Automatic Detection:** New devices, plans, services
✅ **Smart Classification:** Based on context and intent
✅ **Safe Updates:** Automatic backups before changes
✅ **Confidence Scoring:** Only high-quality patterns added
✅ **Learning Logs:** Complete audit trail
✅ **One-Click Update:** Just press the button!

**Your knowledge base now grows automatically with your data!**

---

## Example Workflow

```
1. Upload queries.csv (1000 queries)
   └─ 850 classified, 150 unclassified

2. Click "🧠 Learn & Update Knowledge"
   └─ Analyzes 150 unclassified queries
   └─ Finds 12 new patterns (confidence ≥50)

3. System Updates
   ├─ Backs up decision tree
   ├─ Adds 12 new classifications
   ├─ Saves learning log
   └─ Reloads classifier

4. Reclassify (optional)
   └─ Now 920 classified, 80 unclassified

5. Repeat
   └─ Knowledge base keeps improving!
```

**The more you use it, the smarter it gets!** 🚀
