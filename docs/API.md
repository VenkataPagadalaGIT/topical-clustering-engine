# API Reference

Complete API documentation for the Telecom Query Classification Tool.

---

## Base URL

```
http://localhost:5001
```

---

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible on the local network.

---

## Endpoints

### 1. Upload and Classify

Upload a file containing queries and receive classifications.

```http
POST /upload
```

#### Request

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File | Yes | CSV, Excel (.xlsx, .xls), TSV, or TXT file |

**Content-Type:** `multipart/form-data`

#### Example Request

```bash
curl -X POST http://localhost:5001/upload \
  -F "file=@queries.csv"
```

#### Response

```json
{
  "success": true,
  "summary": {
    "total_queries": 1000,
    "classified_count": 950,
    "unclassified_count": 50,
    "classification_rate": "95.0%",
    "unique_topics": 45,
    "timestamp": "2024-01-15T10:30:00.000Z",
    "top_topics": [
      {"topic": "Unlimited Plan Purchase", "count": 120},
      {"topic": "iPhone Models", "count": 85}
    ],
    "l1_distribution": [
      {"category": "Mobile Plans", "count": 400},
      {"category": "Devices", "count": 350}
    ],
    "intent_distribution": [
      {"intent": "Transactional", "count": 300},
      {"intent": "Informational", "count": 250}
    ],
    "funnel_distribution": [
      {"stage": "Purchase", "count": 200},
      {"stage": "Consideration", "count": 300}
    ]
  },
  "columns_info": {
    "query_column": "Query",
    "other_columns": ["URL", "CPC", "Ranking"],
    "total_rows": 1000,
    "sample_data": [...]
  },
  "results_filename": "results_20240115_103000.csv",
  "data": [
    {
      "original_index": 0,
      "query": "buy unlimited plan",
      "URL": "/plans/unlimited",
      "CPC": 8.50,
      "Ranking": 3,
      "topical_group": "Unlimited Plan Purchase",
      "L1_category": "Mobile Plans",
      "L2_subcategory": "Unlimited Plans",
      "L3_intent": "Transactional",
      "L3_intent_sub": "Direct Purchase Intent",
      "funnel_stage": "Purchase",
      "commercial_score": 95,
      "confidence_score": 0.92,
      "classified": true
    }
  ],
  "total_rows": 1000
}
```

#### Error Response

```json
{
  "error": "Could not detect query column. Please ensure your file has a column named 'Query' or 'Keyword'"
}
```

---

### 2. Download Results

Download the classification results as CSV.

```http
GET /download/{filename}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filename` | String | Yes | Results filename from upload response |

#### Example Request

```bash
curl -O http://localhost:5001/download/results_20240115_103000.csv
```

---

### 3. Export Results

Export results in different formats.

```http
GET /export/{filename}/{format}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filename` | String | Yes | Results filename |
| `format` | String | Yes | Export format: `excel` or `grouped-csv` |

#### Formats

| Format | Description | File Extension |
|--------|-------------|----------------|
| `excel` | Multi-sheet Excel workbook with summaries | .xlsx |
| `grouped-csv` | CSV sorted by L1 > L2 > Topic > Query | .csv |

#### Example Request

```bash
# Excel export
curl -O http://localhost:5001/export/results_20240115_103000.csv/excel

# Grouped CSV export
curl -O http://localhost:5001/export/results_20240115_103000.csv/grouped-csv
```

---

### 4. Get Topic Group Details

Retrieve all queries for a specific topical group.

```http
GET /api/group-details/{filename}/{group_name}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filename` | String | Yes | Results filename |
| `group_name` | String | Yes | Topic group name (URL encoded) |

#### Example Request

```bash
curl "http://localhost:5001/api/group-details/results_20240115_103000.csv/Unlimited%20Plan%20Purchase"
```

#### Response

```json
{
  "group_name": "Unlimited Plan Purchase",
  "count": 45,
  "data": [
    {
      "query": "buy unlimited plan",
      "L1_category": "Mobile Plans",
      "L3_intent": "Transactional",
      "confidence_score": 0.92
    }
  ]
}
```

---

### 5. Submit Feedback

Submit user feedback on a classification.

```http
POST /api/feedback
```

#### Request Body

```json
{
  "query": "buy iphone 15 pro max",
  "classification": {
    "L1": "Devices",
    "L2": "Smartphones",
    "L3": "Transactional",
    "L4": "iPhone Purchase",
    "funnel": "Purchase",
    "score": 95,
    "confidence": 0.88
  },
  "feedback_type": "up",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "filename": "results_20240115_103000.csv"
}
```

#### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | String | Yes | The classified query |
| `classification` | Object | Yes | Classification details |
| `feedback_type` | String | Yes | `up` (correct) or `down` (incorrect) |
| `timestamp` | String | Yes | ISO 8601 timestamp |
| `filename` | String | No | Source results file |

#### Response

```json
{
  "success": true
}
```

---

### 6. Submit Correction

Submit a correction for an incorrect classification.

```http
POST /api/correction
```

#### Request Body

```json
{
  "query": "iphone repair near me",
  "original_classification": "iPhone Purchase",
  "suggested_correction": "Device Repair Services",
  "full_classification": {
    "L1": "Devices",
    "L2": "Smartphones",
    "L3": "Transactional",
    "L4": "iPhone Purchase"
  },
  "filename": "results_20240115_103000.csv",
  "timestamp": "2024-01-15T10:35:00.000Z"
}
```

#### Response

```json
{
  "success": true
}
```

---

### 7. Apply Learning

Analyze unclassified queries and update the knowledge base.

```http
POST /api/learn
```

#### Request Body

```json
{
  "filename": "results_20240115_103000.csv"
}
```

#### Response

```json
{
  "success": true,
  "added_count": 15,
  "backup_path": "learning/backup_20240115_104500.json",
  "new_entities": {
    "devices": ["Pixel 8 Pro", "Galaxy S24"],
    "plans": ["Magenta Max"],
    "services": ["Starlink"],
    "features": []
  },
  "learning_summary": {
    "total_patterns": 850,
    "devices_count": 120,
    "plans_count": 45,
    "services_count": 30
  }
}
```

---

### 8. Get Feedback Data

Retrieve all collected feedback.

```http
GET /api/get-feedback
```

#### Response

```json
{
  "feedback": [
    {
      "query": "buy unlimited plan",
      "classification": {...},
      "feedback_type": "up",
      "timestamp": "2024-01-15T10:30:00.000Z"
    }
  ],
  "count": 150
}
```

---

### 9. Get Corrections

Retrieve all submitted corrections.

```http
GET /api/get-corrections
```

#### Response

```json
{
  "corrections": [
    {
      "timestamp": "2024-01-15T10:35:00.000Z",
      "query": "iphone repair near me",
      "original_L1": "Devices",
      "original_L4": "iPhone Purchase",
      "suggested_correction": "Device Repair Services",
      "filename": "results_20240115_103000.csv"
    }
  ],
  "count": 25
}
```

---

### 10. Export Feedback as Excel

Export all feedback data as an Excel file.

```http
GET /api/export-feedback-excel
```

#### Response

Returns an Excel file download with columns:
- Timestamp
- Query
- L1-L4 Classifications
- Funnel Stage
- Commercial Score
- Confidence
- Feedback Type
- Filename

---

### 11. Validate Corrections

Analyze corrections to find high-confidence patterns.

```http
POST /api/validate
```

#### Response

```json
{
  "success": true,
  "total_corrections": 50,
  "unique_suggestions": 12,
  "high_confidence": [
    {
      "suggested_topic": "Device Repair Services",
      "count": 8,
      "examples": [
        "iphone repair near me",
        "samsung screen repair",
        "phone battery replacement"
      ]
    }
  ]
}
```

---

## Web Pages

### Main Dashboard

```http
GET /
```

The main application interface with:
- Single query classification
- Bulk file upload
- Sample data testing

### Feedback Viewer

```http
GET /feedback-viewer
```

Interface for viewing and managing collected feedback.

### Test Upload

```http
GET /test-upload
```

Simplified upload interface for debugging.

---

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input or missing required fields |
| 404 | Not Found - File or resource not found |
| 500 | Internal Server Error - Processing error |

---

## Rate Limits

Currently, there are no rate limits. For production deployment, consider implementing:
- Request rate limiting
- File size restrictions
- Concurrent upload limits

---

## Data Formats

### Supported Input Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| CSV | .csv | UTF-8 or Latin-1 encoding |
| Excel | .xlsx, .xls | First sheet is used |
| TSV | .tsv | Tab-separated values |
| TXT | .txt | One query per line |

### Query Column Detection

The system automatically detects the query column by looking for:
1. Exact match: `query`, `keyword`, `keywords`, `search term`
2. Partial match: Column names containing these words
3. Fallback: First text column

---

## Python SDK Example

```python
import requests

class TelecomClassifierClient:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url

    def classify_file(self, filepath):
        """Upload and classify a file."""
        with open(filepath, 'rb') as f:
            response = requests.post(
                f"{self.base_url}/upload",
                files={'file': f}
            )
        return response.json()

    def classify_query(self, query):
        """Classify a single query."""
        import io
        csv_content = f"Query\n{query}"
        response = requests.post(
            f"{self.base_url}/upload",
            files={'file': ('query.csv', io.StringIO(csv_content))}
        )
        data = response.json()
        return data['data'][0] if data.get('data') else None

    def export_excel(self, filename):
        """Export results as Excel."""
        response = requests.get(
            f"{self.base_url}/export/{filename}/excel"
        )
        return response.content

    def submit_feedback(self, query, classification, feedback_type):
        """Submit feedback on a classification."""
        response = requests.post(
            f"{self.base_url}/api/feedback",
            json={
                'query': query,
                'classification': classification,
                'feedback_type': feedback_type,
                'timestamp': datetime.now().isoformat()
            }
        )
        return response.json()

# Usage
client = TelecomClassifierClient()

# Classify a file
results = client.classify_file("queries.csv")
print(f"Classified {results['summary']['total_queries']} queries")

# Classify single query
result = client.classify_query("buy unlimited data plan")
print(f"Topic: {result['topical_group']}")
```

---

## Webhook Integration (Future)

For real-time notifications, webhook support is planned:

```json
{
  "webhook_url": "https://your-server.com/webhook",
  "events": ["classification_complete", "learning_applied"]
}
```
