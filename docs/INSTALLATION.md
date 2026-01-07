# Installation Guide

Complete guide to installing and configuring the Topical Clustering Engine.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Installation](#quick-installation)
3. [Detailed Installation](#detailed-installation)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)
7. [Production Deployment](#production-deployment)

---

## System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | macOS 10.15+, Ubuntu 18.04+, Windows 10+ |
| **Python** | 3.9 or higher |
| **RAM** | 4 GB minimum |
| **Storage** | 500 MB for application + data |
| **CPU** | 2 cores recommended |

### Recommended Requirements

| Component | Recommendation |
|-----------|----------------|
| **Python** | 3.11+ |
| **RAM** | 8 GB+ for large datasets |
| **Storage** | SSD for better performance |
| **CPU** | 4+ cores for parallel processing |

---

## Quick Installation

For experienced users, here's the fastest way to get started:

```bash
# Clone and setup
git clone https://github.com/VenkataPagadalaGIT/telecom-query-classifier.git
cd telecom-query-classifier
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python app.py

# Open http://localhost:5001
```

---

## Detailed Installation

### Step 1: Install Python

#### macOS

```bash
# Using Homebrew (recommended)
brew install python@3.11

# Verify installation
python3 --version
```

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Verify installation
python3.11 --version
```

#### Windows

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer with "Add Python to PATH" checked
3. Verify in Command Prompt:
   ```cmd
   python --version
   ```

---

### Step 2: Clone the Repository

```bash
# Using HTTPS
git clone https://github.com/VenkataPagadalaGIT/topical-clustering-engine.git

# Or using SSH
git clone git@github.com:VenkataPagadalaGIT/topical-clustering-engine.git

# Navigate to project
cd topical-clustering-engine
```

---

### Step 3: Create Virtual Environment

#### macOS/Linux

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (should show venv path)
which python
```

#### Windows

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify activation
where python
```

---

### Step 4: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

#### Dependencies Installed

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 2.0+ | Web framework |
| pandas | 1.5+ | Data processing |
| openpyxl | 3.0+ | Excel export |
| Werkzeug | 2.0+ | WSGI utilities |

---

### Step 5: Verify Installation

```bash
# Check all dependencies are installed
pip list

# Test the classifier module
python -c "from telecom_classifier import TelecomClassifier; print('OK')"

# Test Flask app import
python -c "from app import app; print('OK')"
```

---

## Configuration

### Environment Variables

Create a `.env` file (optional):

```bash
# .env file
PORT=5001
DEBUG=True
MAX_CONTENT_LENGTH=104857600  # 100MB
UPLOAD_FOLDER=uploads
RESULTS_FOLDER=results
LEARNING_FOLDER=learning
```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 5001 | Server port |
| `DEBUG` | True | Enable debug mode |
| `MAX_CONTENT_LENGTH` | 100MB | Maximum upload size |
| `UPLOAD_FOLDER` | uploads | Directory for uploads |
| `RESULTS_FOLDER` | results | Directory for results |
| `LEARNING_FOLDER` | learning | Directory for learning data |

### Knowledge Base Configuration

The classification knowledge base is stored in:
```
telecom-classification-EXPANDED.json
```

To customize:
1. Edit the JSON file directly
2. Add new keywords to L5
3. Add new topics to L4
4. Restart the application

---

## Running the Application

### Development Mode

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run with default port (5001)
python app.py

# Run with custom port
python app.py 8080
```

### Access the Application

| Interface | URL |
|-----------|-----|
| Main Dashboard | http://localhost:5001 |
| Feedback Viewer | http://localhost:5001/feedback-viewer |
| API Base | http://localhost:5001/api |

### Using the Start Script

```bash
# Make script executable
chmod +x start_app.sh

# Run the script
./start_app.sh
```

---

## Directory Structure After Installation

```
topical-clustering-engine/
├── venv/                    # Virtual environment (created)
├── uploads/                 # Uploaded files (created on first use)
├── results/                 # Classification results (created)
├── learning/                # Learning data (created)
│   ├── feedback/           # User feedback
│   └── corrections/        # User corrections
├── app.py                  # Main application
├── telecom_classifier.py   # Classification engine
├── learning_engine.py      # Learning system
├── requirements.txt        # Dependencies
├── telecom-classification-EXPANDED.json  # Knowledge base
├── templates/              # HTML templates
├── static/                 # Static files
└── docs/                   # Documentation
```

---

## Troubleshooting

### Common Issues

#### 1. "Module not found" Error

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. Port Already in Use

```bash
# Find process using port
lsof -i :5001

# Kill the process
kill -9 <PID>

# Or use a different port
python app.py 8080
```

#### 3. Permission Denied

```bash
# Fix file permissions
chmod +x app.py
chmod +x start_app.sh
```

#### 4. Knowledge Base Not Found

```bash
# Verify the JSON file exists
ls -la telecom-classification-EXPANDED.json

# Create symlink if needed
ln -s telecom-classification-EXPANDED.json telecom-classification.json
```

#### 5. Excel Export Fails

```bash
# Install openpyxl
pip install openpyxl

# Verify installation
python -c "import openpyxl; print('OK')"
```

### Debug Mode

Enable verbose logging:

```python
# In app.py, set:
app.run(debug=True, host='0.0.0.0', port=5001)
```

Check logs:
```bash
tail -f app.log
```

---

## Production Deployment

### Using Gunicorn (Recommended)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### Using Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app"]
```

```bash
# Build and run
docker build -t telecom-classifier .
docker run -p 5001:5001 telecom-classifier
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    client_max_body_size 100M;
}
```

### Systemd Service

```ini
# /etc/systemd/system/telecom-classifier.service
[Unit]
Description=Telecom Query Classifier
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/telecom-classifier
Environment="PATH=/opt/telecom-classifier/venv/bin"
ExecStart=/opt/telecom-classifier/venv/bin/gunicorn -w 4 -b 127.0.0.1:5001 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable telecom-classifier
sudo systemctl start telecom-classifier
```

---

## Updating

### Update to Latest Version

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart application
python app.py
```

### Backup Before Update

```bash
# Backup knowledge base
cp telecom-classification-EXPANDED.json telecom-classification-EXPANDED.json.bak

# Backup learning data
cp -r learning/ learning_backup/
```

---

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove project directory
cd ..
rm -rf telecom-query-classifier

# Remove any global packages (if installed)
pip uninstall flask pandas openpyxl
```

---

## Support

If you encounter issues:

1. Check this troubleshooting guide
2. Search [GitHub Issues](https://github.com/VenkataPagadalaGIT/topical-clustering-engine/issues)
3. Create a new issue with:
   - Error message
   - Python version
   - Operating system
   - Steps to reproduce
