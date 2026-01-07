<p align="center">
  <img src="docs/screenshots/logo.png" alt="Telecom Query Classifier" width="120">
</p>

<h1 align="center">Telecom Query Classification Tool</h1>

<p align="center">
  <strong>Enterprise-grade search query classification with 5-level hierarchical taxonomy</strong>
</p>

<p align="center">
  <a href="#features"><img src="https://img.shields.io/badge/Features-12+-red.svg" alt="Features"></a>
  <a href="#installation"><img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python"></a>
  <a href="#api-reference"><img src="https://img.shields.io/badge/API-REST-green.svg" alt="API"></a>
  <a href="#license"><img src="https://img.shields.io/badge/License-MIT-purple.svg" alt="License"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="#features">Features</a> •
  <a href="#screenshots">Screenshots</a> •
  <a href="#api-reference">API</a> •
  <a href="#documentation">Docs</a>
</p>

---

## Overview

The **Telecom Query Classification Tool** is a production-ready web application that automatically classifies telecom-related search queries into a comprehensive 5-level hierarchical taxonomy. Designed for SEO professionals, content strategists, and data analysts in the telecommunications industry.

### Why This Tool?

| Challenge | Solution |
|-----------|----------|
| Manual keyword grouping takes hours | **Instant classification** of 10,000+ queries |
| Inconsistent categorization | **Standardized 5-level taxonomy** |
| No intent understanding | **Automatic intent detection** with commercial scoring |
| Static keyword lists | **Self-learning engine** that improves over time |

---

## Screenshots

### Dashboard - Single Query Classification
<p align="center">
  <img src="docs/screenshots/single-query.png" alt="Single Query Classification" width="800">
</p>

*Instant classification with confidence scores, intent analysis, and funnel stage mapping*

### Bulk Upload & Processing
<p align="center">
  <img src="docs/screenshots/bulk-upload.png" alt="Bulk Upload" width="800">
</p>

*Drag & drop CSV/Excel files for batch processing of thousands of queries*

### Classification Results
<p align="center">
  <img src="docs/screenshots/results-table.png" alt="Results Table" width="800">
</p>

*Interactive data table with filtering, sorting, and feedback collection*

### Topic Clustering View
<p align="center">
  <img src="docs/screenshots/grouped-view.png" alt="Grouped View" width="800">
</p>

*Collapsible topic clusters with query counts and metadata*

---

## Features

### Core Classification Engine

- **5-Level Hierarchical Taxonomy**
  - L1: Broad Categories (7 total)
  - L2: Subcategories (360 total)
  - L3: Search Intent (36 types)
  - L4: Specific Topics (400+)
  - L5: Individual Keywords (800+)

- **Intent Detection**
  - Transactional, Informational, Navigational
  - Commercial Investigation, Local Search
  - Customer Support queries

- **Commercial Scoring**
  - 0-100 business value score
  - Conversion probability estimates
  - Funnel stage mapping

### Data Processing

| Feature | Capability |
|---------|------------|
| **File Formats** | CSV, Excel (.xlsx, .xls), TSV, TXT |
| **Max File Size** | 100 MB |
| **Processing Speed** | ~1,000 queries/second |
| **Batch Size** | 100,000+ queries |

### Learning System

- **User Feedback** - Thumbs up/down on classifications
- **Correction Tracking** - Suggest better classifications
- **Pattern Learning** - Automatic knowledge base updates
- **Version Control** - Backup before every update

### Export Options

- **Excel** - Multi-sheet workbook with summaries
- **Grouped CSV** - Sorted by topic hierarchy
- **JSON API** - Programmatic access

---

## Quick Start

### Prerequisites

- Python 3.9+
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/VenkataPagadalaGIT/telecom-query-classifier.git
cd telecom-query-classifier

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the application
python app.py
```

### Access

| Interface | URL |
|-----------|-----|
| **Main Dashboard** | http://localhost:5001 |
| **Feedback Viewer** | http://localhost:5001/feedback-viewer |

---

## Classification Taxonomy

### L1 Categories

| Category | Monthly Search Volume | Business Value |
|----------|----------------------|----------------|
| Mobile Plans | 2.1M | Very High |
| Devices | 1.8M | Very High |
| Internet Services | 950K | High |
| TV & Streaming | 620K | Medium |
| Business Solutions | 340K | High |
| Support & Account | 890K | Medium |
| Promotions | 450K | High |

### L3 Intent Types

| Intent | Commercial Score | Funnel Stage | Example |
|--------|------------------|--------------|---------|
| Transactional | 85-100 | Purchase | "buy unlimited plan" |
| Commercial Investigation | 60-84 | Consideration | "best 5g phones 2024" |
| Comparative | 65-80 | Evaluation | "verizon vs tmobile" |
| Informational | 30-59 | Awareness | "what is 5g" |
| Local | 50-80 | Decision | "tmobile store near me" |
| Support | 15-35 | Retention | "reset voicemail password" |

---

## API Reference

### Upload & Classify

```http
POST /upload
Content-Type: multipart/form-data

file: <CSV or Excel file>
```

**Response:**
```json
{
  "success": true,
  "summary": {
    "total_queries": 1000,
    "classified_count": 950,
    "classification_rate": "95.0%",
    "unique_topics": 45
  },
  "results_filename": "results_20240101_120000.csv",
  "data": [
    {
      "query": "buy unlimited plan",
      "topical_group": "Unlimited Plan Purchase",
      "L1_category": "Mobile Plans",
      "L2_subcategory": "Unlimited Plans",
      "L3_intent": "Transactional",
      "funnel_stage": "Purchase",
      "commercial_score": 95,
      "confidence_score": 0.92
    }
  ]
}
```

### Export Results

```http
GET /export/{filename}/{format}
```

| Format | Description |
|--------|-------------|
| `excel` | Multi-sheet Excel workbook |
| `grouped-csv` | CSV sorted by topic hierarchy |

### Submit Feedback

```http
POST /api/feedback
Content-Type: application/json

{
  "query": "buy iphone 15",
  "classification": {
    "L1": "Devices",
    "L2": "Smartphones",
    "L3": "Transactional",
    "L4": "iPhone Purchase"
  },
  "feedback_type": "up",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Apply Learning

```http
POST /api/learn
Content-Type: application/json

{
  "filename": "results_20240101_120000.csv"
}
```

---

## File Structure

```
telecom-query-classifier/
├── app.py                          # Flask web application
├── telecom_classifier.py           # Classification engine
├── learning_engine.py              # Adaptive learning system
├── requirements.txt                # Python dependencies
├── telecom-classification-EXPANDED.json  # Knowledge base (3,800+ keywords)
│
├── templates/
│   ├── index.html                  # Main dashboard (red theme)
│   ├── feedback_viewer.html        # Feedback management
│   └── test_upload_simple.html     # Debug interface
│
├── static/
│   ├── sample_queries.csv          # 40 sample queries
│   └── sample_queries_100.csv      # 100 extended samples
│
├── docs/
│   ├── API.md                      # API documentation
│   ├── INSTALLATION.md             # Detailed setup guide
│   └── screenshots/                # Application screenshots
│
├── uploads/                        # Uploaded files (gitignored)
├── results/                        # Classification results (gitignored)
└── learning/                       # Learning data (gitignored)
```

---

## Configuration

### Server Options

```bash
# Custom port
python app.py 8080

# Production mode
FLASK_ENV=production python app.py
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 5001 | Server port |
| `MAX_CONTENT_LENGTH` | 100MB | Max upload size |
| `DEBUG` | True | Debug mode |

---

## Performance Benchmarks

| Metric | Value |
|--------|-------|
| Single Query | <50ms |
| 1,000 Queries | ~2 seconds |
| 10,000 Queries | ~15 seconds |
| 100,000 Queries | ~2.5 minutes |
| Memory Usage | ~100MB base |
| Concurrent Users | 50+ |

---

## Use Cases

### SEO Content Strategy
- Group keywords by topic clusters
- Identify content gaps
- Prioritize by commercial value
- Map to marketing funnel

### PPC Campaign Organization
- Segment by search intent
- Group into ad groups by topic
- Optimize bids by commercial score
- Track funnel position

### Competitive Analysis
- Upload competitor keywords
- Analyze their topical focus
- Find coverage gaps
- Benchmark classification rates

---

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Documentation

| Document | Description |
|----------|-------------|
| [API.md](docs/API.md) | Complete API reference |
| [INSTALLATION.md](docs/INSTALLATION.md) | Detailed setup guide |
| [LEARNING_SYSTEM.md](LEARNING_SYSTEM.md) | How the learning engine works |
| [QA_QUICK_START.md](QA_QUICK_START.md) | Quality assurance guide |

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support

- **Issues**: [GitHub Issues](https://github.com/VenkataPagadalaGIT/telecom-query-classifier/issues)
- **Documentation**: [docs/](docs/)

---

<p align="center">
  <strong>Built for SEO Professionals</strong><br>
  <a href="https://github.com/VenkataPagadalaGIT/telecom-query-classifier/issues">Report Bug</a> •
  <a href="https://github.com/VenkataPagadalaGIT/telecom-query-classifier/issues">Request Feature</a>
</p>
