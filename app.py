#!/usr/bin/env python3
"""
Telecom Query Grouping Web Application
Upload CSV with queries + metadata, get topical groupings
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import sys

# Import our classifier and learning engine
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from telecom_classifier import TelecomClassifier
from learning_engine import LearningEngine

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'
app.config['LEARNING_FOLDER'] = 'learning'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xlsx', 'xls', 'tsv', 'txt'}

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)
os.makedirs(app.config['LEARNING_FOLDER'], exist_ok=True)

# Initialize classifier and learning engine
DECISION_TREE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'telecom-classification.json')
classifier = TelecomClassifier(DECISION_TREE_PATH)
learning_engine = LearningEngine(DECISION_TREE_PATH)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def read_upload_file(filepath):
    """Read uploaded file into DataFrame"""
    ext = filepath.rsplit('.', 1)[1].lower()

    try:
        if ext == 'csv':
            # Try different encodings and delimiters
            try:
                df = pd.read_csv(filepath, encoding='utf-8')
            except:
                try:
                    df = pd.read_csv(filepath, encoding='latin1')
                except:
                    df = pd.read_csv(filepath, encoding='utf-8', sep='\t')
        elif ext in ['xlsx', 'xls']:
            df = pd.read_excel(filepath)
        elif ext == 'tsv':
            df = pd.read_csv(filepath, sep='\t')
        elif ext == 'txt':
            # Assume one query per line
            with open(filepath, 'r', encoding='utf-8') as f:
                queries = [line.strip() for line in f if line.strip()]
            df = pd.DataFrame({'Query': queries})
        else:
            return None

        return df
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def detect_query_column(df):
    """Detect which column contains the queries/keywords"""
    possible_names = ['query', 'keyword', 'keywords', 'search term', 'search query',
                     'term', 'queries', 'search', 'phrase', 'key phrase']

    # Check exact matches (case-insensitive)
    for col in df.columns:
        if col.lower() in possible_names:
            return col

    # Check partial matches
    for col in df.columns:
        for name in possible_names:
            if name in col.lower():
                return col

    # Default to first column if text-heavy
    if len(df.columns) > 0:
        first_col = df.columns[0]
        # Check if first column looks like queries (mostly strings, reasonable length)
        if df[first_col].dtype == 'object':
            return first_col

    return None


def classify_queries(df, query_column):
    """Classify all queries in the dataframe"""
    results = []

    for idx, row in df.iterrows():
        query = str(row[query_column]).strip()

        if not query or query.lower() in ['nan', 'none', '']:
            # Skip empty queries
            classification = None
        else:
            classification = classifier.classify_text(query)

        # Build result row
        result = {
            'original_index': idx,
            'query': query,
        }

        # Add all original columns
        for col in df.columns:
            if col != query_column:
                result[col] = row[col]

        # Add classification if found
        if classification:
            result['topical_group'] = classification['classification']['L4']['topic']
            result['L1_category'] = classification['classification']['L1']['name']
            result['L2_subcategory'] = classification['classification']['L2']['name']
            result['L3_intent'] = classification['classification']['L3']['intent_category']
            result['L3_intent_sub'] = classification['classification']['L3']['intent_subcategory']
            result['funnel_stage'] = classification['classification']['L3']['funnel_stage']
            result['commercial_score'] = classification['classification']['L3']['commercial_score']
            result['confidence_score'] = round(classification['confidence_score'], 2)
            result['classified'] = True
        else:
            result['topical_group'] = 'Unclassified'
            result['L1_category'] = 'N/A'
            result['L2_subcategory'] = 'N/A'
            result['L3_intent'] = 'N/A'
            result['L3_intent_sub'] = 'N/A'
            result['funnel_stage'] = 'N/A'
            result['commercial_score'] = 0
            result['confidence_score'] = 0
            result['classified'] = False

        results.append(result)

    return pd.DataFrame(results)


def generate_summary(df):
    """Generate summary statistics"""
    total = len(df)
    classified = df['classified'].sum()

    summary = {
        'total_queries': total,
        'classified_count': int(classified),
        'unclassified_count': int(total - classified),
        'classification_rate': f"{(classified / total * 100):.1f}%" if total > 0 else "0%",
        'unique_topics': len(df[df['classified'] == True]['topical_group'].unique()),
        'timestamp': datetime.now().isoformat()
    }

    # Group by topical group
    topical_groups = df[df['classified'] == True].groupby('topical_group').size().sort_values(ascending=False)
    summary['top_topics'] = [
        {'topic': topic, 'count': int(count)}
        for topic, count in topical_groups.head(10).items()
    ]

    # Group by L1 category
    l1_groups = df[df['classified'] == True].groupby('L1_category').size().sort_values(ascending=False)
    summary['l1_distribution'] = [
        {'category': cat, 'count': int(count)}
        for cat, count in l1_groups.items()
    ]

    # Intent distribution
    intent_groups = df[df['classified'] == True].groupby('L3_intent').size().sort_values(ascending=False)
    summary['intent_distribution'] = [
        {'intent': intent, 'count': int(count)}
        for intent, count in intent_groups.items()
    ]

    # Funnel stage distribution
    funnel_groups = df[df['classified'] == True].groupby('funnel_stage').size().sort_values(ascending=False)
    summary['funnel_distribution'] = [
        {'stage': stage, 'count': int(count)}
        for stage, count in funnel_groups.items()
    ]

    return summary


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and classification"""

    # Check if file is present
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload CSV, Excel, or TXT file'}), 400

    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        saved_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
        file.save(filepath)

        # Read file
        df = read_upload_file(filepath)
        if df is None:
            return jsonify({'error': 'Could not read file. Please check format'}), 400

        # Detect query column
        query_column = detect_query_column(df)
        if query_column is None:
            return jsonify({'error': 'Could not detect query column. Please ensure your file has a column named "Query" or "Keyword"'}), 400

        # Get column info for frontend
        columns_info = {
            'query_column': query_column,
            'other_columns': [col for col in df.columns if col != query_column],
            'total_rows': len(df),
            'sample_data': df.head(5).to_dict('records')
        }

        # Classify queries
        results_df = classify_queries(df, query_column)

        # Generate summary
        summary = generate_summary(results_df)

        # Save results
        results_filename = f"results_{timestamp}.csv"
        results_path = os.path.join(app.config['RESULTS_FOLDER'], results_filename)
        results_df.to_csv(results_path, index=False)

        # Prepare data for frontend (replace NaN with None for JSON)
        results_df_clean = results_df.fillna('')

        response = {
            'success': True,
            'summary': summary,
            'columns_info': columns_info,
            'results_filename': results_filename,
            'data': results_df_clean.to_dict('records')[:100],  # Send first 100 rows
            'total_rows': len(results_df)
        }

        return jsonify(response)

    except Exception as e:
        print(f"Error processing file: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500


@app.route('/download/<filename>')
def download_file(filename):
    """Download results file"""
    filepath = os.path.join(app.config['RESULTS_FOLDER'], filename)

    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    return send_file(filepath, as_attachment=True)


@app.route('/export/<filename>/<format>')
def export_file(filename, format):
    """Export results in different formats"""
    filepath = os.path.join(app.config['RESULTS_FOLDER'], filename)

    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    df = pd.read_csv(filepath)

    if format == 'excel':
        # Export to Excel with multiple sheets
        output_filename = filename.replace('.csv', '.xlsx')
        output_path = os.path.join(app.config['RESULTS_FOLDER'], output_filename)

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # All data
            df.to_excel(writer, sheet_name='All Data', index=False)

            # Grouped by topic
            if 'topical_group' in df.columns:
                topic_summary = df.groupby('topical_group').size().reset_index(name='count')
                topic_summary = topic_summary.sort_values('count', ascending=False)
                topic_summary.to_excel(writer, sheet_name='Topics Summary', index=False)

            # Grouped by L1
            if 'L1_category' in df.columns:
                l1_summary = df.groupby('L1_category').size().reset_index(name='count')
                l1_summary = l1_summary.sort_values('count', ascending=False)
                l1_summary.to_excel(writer, sheet_name='L1 Categories', index=False)

        return send_file(output_path, as_attachment=True)

    elif format == 'grouped-csv':
        # Export CSV sorted by topical group
        df_sorted = df.sort_values(['L1_category', 'L2_subcategory', 'topical_group', 'query'])
        output_filename = filename.replace('.csv', '_grouped.csv')
        output_path = os.path.join(app.config['RESULTS_FOLDER'], output_filename)
        df_sorted.to_csv(output_path, index=False)

        return send_file(output_path, as_attachment=True)

    else:
        return jsonify({'error': 'Invalid format'}), 400


@app.route('/api/group-details/<filename>/<group_name>')
def get_group_details(filename, group_name):
    """Get all queries for a specific topical group"""
    filepath = os.path.join(app.config['RESULTS_FOLDER'], filename)

    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    df = pd.read_csv(filepath)
    group_data = df[df['topical_group'] == group_name]

    return jsonify({
        'group_name': group_name,
        'count': len(group_data),
        'data': group_data.to_dict('records')
    })


@app.route('/api/learn', methods=['POST'])
def apply_learning():
    """Analyze unclassified queries and update decision tree"""
    try:
        data = request.json
        filename = data.get('filename')

        if not filename:
            return jsonify({'error': 'Filename required'}), 400

        filepath = os.path.join(app.config['RESULTS_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404

        # Read results
        df = pd.read_csv(filepath)

        # Get unclassified queries
        unclassified = df[df['classified'] == False]

        if len(unclassified) == 0:
            return jsonify({
                'success': True,
                'message': 'No unclassified queries to learn from',
                'added_count': 0
            })

        # Analyze each unclassified query
        suggestions = []
        for _, row in unclassified.iterrows():
            query = row['query']
            learned_info = learning_engine.analyze_unclassified(query)

            if learned_info:
                suggestion = learning_engine.suggest_new_classification(query, learned_info)
                if suggestion.get('confidence', 0) >= 50:
                    suggestions.append(suggestion)

        # Update decision tree
        if suggestions:
            result = learning_engine.update_decision_tree(suggestions, min_confidence=50)

            # Reload classifier with updated tree
            global classifier
            classifier = TelecomClassifier(DECISION_TREE_PATH)

            # Save learning log
            learning_log_path = os.path.join(app.config['LEARNING_FOLDER'],
                                           f"learning_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(learning_log_path, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'unclassified_count': len(unclassified),
                    'suggestions': suggestions,
                    'result': result
                }, f, indent=2)

            return jsonify({
                'success': True,
                'added_count': result['added_count'],
                'backup_path': result['backup_path'],
                'new_entities': result['new_entities'],
                'learning_summary': learning_engine.get_learning_summary()
            })
        else:
            return jsonify({
                'success': True,
                'message': 'No high-confidence patterns found',
                'added_count': 0
            })

    except Exception as e:
        print(f"Error in learning: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/feedback', methods=['POST'])
def save_feedback():
    """Save user feedback on classifications"""
    try:
        data = request.json

        # Create feedback directory if not exists
        feedback_dir = os.path.join(app.config['LEARNING_FOLDER'], 'feedback')
        os.makedirs(feedback_dir, exist_ok=True)

        # Save feedback with timestamp
        feedback_file = os.path.join(feedback_dir, f"feedback_{datetime.now().strftime('%Y%m%d')}.jsonl")
        with open(feedback_file, 'a') as f:
            f.write(json.dumps(data) + '\n')

        return jsonify({'success': True})
    except Exception as e:
        print(f"Error saving feedback: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/correction', methods=['POST'])
def save_correction():
    """Save user corrections for false positives"""
    try:
        data = request.json

        # Create corrections directory
        corrections_dir = os.path.join(app.config['LEARNING_FOLDER'], 'corrections')
        os.makedirs(corrections_dir, exist_ok=True)

        # Save correction
        correction_file = os.path.join(corrections_dir, f"corrections_{datetime.now().strftime('%Y%m%d')}.jsonl")
        with open(correction_file, 'a') as f:
            f.write(json.dumps(data) + '\n')

        # Also update a master corrections file for easy review
        master_file = os.path.join(corrections_dir, 'corrections_master.csv')
        correction_df = pd.DataFrame([{
            'timestamp': data['timestamp'],
            'query': data['query'],
            'original_L1': data['full_classification']['L1'],
            'original_L2': data['full_classification']['L2'],
            'original_L3': data['full_classification']['L3'],
            'original_L4': data['full_classification']['L4'],
            'suggested_correction': data['suggested_correction'],
            'filename': data['filename']
        }])

        if os.path.exists(master_file):
            existing_df = pd.read_csv(master_file)
            correction_df = pd.concat([existing_df, correction_df], ignore_index=True)

        correction_df.to_csv(master_file, index=False)

        return jsonify({'success': True})
    except Exception as e:
        print(f"Error saving correction: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/validate', methods=['POST'])
def validate_with_ai():
    """Validate corrections and learn from mistakes using Claude AI (placeholder)"""
    try:
        data = request.json

        # Get all corrections from today
        corrections_dir = os.path.join(app.config['LEARNING_FOLDER'], 'corrections')
        correction_file = os.path.join(corrections_dir, f"corrections_{datetime.now().strftime('%Y%m%d')}.jsonl")

        if not os.path.exists(correction_file):
            return jsonify({'success': True, 'message': 'No corrections to validate'})

        # Read corrections
        corrections = []
        with open(correction_file, 'r') as f:
            for line in f:
                corrections.append(json.loads(line))

        # Group by suggested correction to find patterns
        correction_patterns = {}
        for corr in corrections:
            suggested = corr['suggested_correction']
            if suggested not in correction_patterns:
                correction_patterns[suggested] = []
            correction_patterns[suggested].append(corr)

        # Find high-confidence corrections (multiple users suggesting the same thing)
        high_confidence_corrections = []
        for suggested, items in correction_patterns.items():
            if len(items) >= 2:  # At least 2 users suggested this correction
                high_confidence_corrections.append({
                    'suggested_topic': suggested,
                    'count': len(items),
                    'examples': [item['query'] for item in items[:5]]
                })

        # TODO: Integrate with Claude AI API for validation
        # This is a placeholder for future Claude AI integration

        return jsonify({
            'success': True,
            'total_corrections': len(corrections),
            'unique_suggestions': len(correction_patterns),
            'high_confidence': high_confidence_corrections
        })

    except Exception as e:
        print(f"Error in validation: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/get-feedback', methods=['GET'])
def get_feedback():
    """Get all feedback data"""
    try:
        feedback_dir = os.path.join(app.config['LEARNING_FOLDER'], 'feedback')
        all_feedback = []

        if os.path.exists(feedback_dir):
            for filename in os.listdir(feedback_dir):
                if filename.endswith('.jsonl'):
                    filepath = os.path.join(feedback_dir, filename)
                    with open(filepath, 'r') as f:
                        for line in f:
                            if line.strip():
                                all_feedback.append(json.loads(line))

        return jsonify({'feedback': all_feedback, 'count': len(all_feedback)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/get-corrections', methods=['GET'])
def get_corrections():
    """Get all corrections data"""
    try:
        corrections_file = os.path.join(app.config['LEARNING_FOLDER'], 'corrections', 'corrections_master.csv')

        if os.path.exists(corrections_file):
            df = pd.read_csv(corrections_file)
            corrections = df.to_dict('records')
            return jsonify({'corrections': corrections, 'count': len(corrections)})
        else:
            return jsonify({'corrections': [], 'count': 0})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export-feedback-excel', methods=['GET'])
def export_feedback_excel():
    """Export feedback as Excel file"""
    try:
        feedback_dir = os.path.join(app.config['LEARNING_FOLDER'], 'feedback')
        all_feedback = []

        if os.path.exists(feedback_dir):
            for filename in os.listdir(feedback_dir):
                if filename.endswith('.jsonl'):
                    filepath = os.path.join(feedback_dir, filename)
                    with open(filepath, 'r') as f:
                        for line in f:
                            if line.strip():
                                feedback = json.loads(line)
                                all_feedback.append({
                                    'Timestamp': feedback['timestamp'],
                                    'Query': feedback['query'],
                                    'L1 Category': feedback['classification']['L1'],
                                    'L2 Subcategory': feedback['classification']['L2'],
                                    'L3 Intent': feedback['classification']['L3'],
                                    'L4 Topic': feedback['classification']['L4'],
                                    'Funnel Stage': feedback['classification']['funnel'],
                                    'Commercial Score': feedback['classification']['score'],
                                    'Confidence': feedback['classification']['confidence'],
                                    'Feedback Type': feedback['feedback_type'],
                                    'Filename': feedback.get('filename', 'N/A')
                                })

        df = pd.DataFrame(all_feedback)

        # Save to Excel
        excel_path = os.path.join(app.config['RESULTS_FOLDER'], f'feedback_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')
        df.to_excel(excel_path, index=False)

        return send_file(excel_path, as_attachment=True, download_name=f'feedback_export_{datetime.now().strftime("%Y%m%d")}.xlsx')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/feedback-viewer')
def feedback_viewer():
    """Feedback viewer page"""
    return render_template('feedback_viewer.html')


@app.route('/test-upload')
def test_upload():
    """Test upload page for debugging"""
    return render_template('test_upload_simple.html')


if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001

    print("=" * 80)
    print("Telecom Query Grouping Web App")
    print("=" * 80)
    print(f"Starting server at http://localhost:{port}")
    print(f"Upload your CSV/Excel file with queries and metadata")
    print(f"Decision tree: {DECISION_TREE_PATH}")
    print("=" * 80)
    print(f"📊 Feedback Viewer: http://localhost:{port}/feedback-viewer")
    print("=" * 80)

    app.run(debug=True, host='0.0.0.0', port=port)
