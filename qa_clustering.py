#!/usr/bin/env python3
"""
QA Clustering System for Telecom Query Classification
Analyzes quality, groups similar queries, identifies issues

Usage:
    python3 qa_clustering.py
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score, calinski_harabasz_score


class QAClusteringEngine:
    """
    Main engine for QA clustering analysis
    """

    def __init__(self, results_folder='results', learning_folder='learning'):
        self.results_folder = results_folder
        self.learning_folder = learning_folder
        self.data = None
        self.feedback_data = None
        self.corrections_data = None
        self.clusters = None
        self.quality_metrics = {}
        self.cluster_analysis = None

    def load_classification_data(self):
        """Load all classified query results"""
        print("📂 Loading classification data...")

        # Find latest results file
        results_files = [f for f in os.listdir(self.results_folder) if f.startswith('results_') and f.endswith('.csv')]

        if not results_files:
            raise FileNotFoundError("No results files found in 'results/' folder")

        latest_file = sorted(results_files)[-1]
        filepath = os.path.join(self.results_folder, latest_file)

        print(f"   Loading: {latest_file}")
        self.data = pd.read_csv(filepath)

        print(f"✅ Loaded {len(self.data)} queries")
        print(f"   Columns: {list(self.data.columns)}")

        return self.data

    def load_feedback_data(self):
        """Load user feedback from JSONL files"""
        print("📂 Loading feedback data...")

        feedback_dir = os.path.join(self.learning_folder, 'feedback')
        all_feedback = []

        if os.path.exists(feedback_dir):
            for filename in os.listdir(feedback_dir):
                if filename.endswith('.jsonl'):
                    filepath = os.path.join(feedback_dir, filename)
                    with open(filepath, 'r') as f:
                        for line in f:
                            if line.strip():
                                all_feedback.append(json.loads(line))

        self.feedback_data = pd.DataFrame(all_feedback) if all_feedback else pd.DataFrame()

        print(f"✅ Loaded {len(self.feedback_data)} feedback entries")

        return self.feedback_data

    def load_corrections_data(self):
        """Load user corrections from CSV"""
        print("📂 Loading corrections data...")

        corrections_file = os.path.join(self.learning_folder, 'corrections', 'corrections_master.csv')

        if os.path.exists(corrections_file):
            self.corrections_data = pd.read_csv(corrections_file)
            print(f"✅ Loaded {len(self.corrections_data)} corrections")
            return self.corrections_data
        else:
            print("⚠️  No corrections file found")
            self.corrections_data = pd.DataFrame()
            return self.corrections_data

    def analyze_data_quality(self):
        """Analyze overall data quality metrics"""
        print("\n📊 Analyzing Data Quality...")

        if self.data is None:
            raise ValueError("No data loaded. Call load_classification_data() first")

        metrics = {}

        # Classification coverage
        classified = self.data[self.data['topical_group'] != 'Unclassified']
        metrics['total_queries'] = len(self.data)
        metrics['classified_count'] = len(classified)
        metrics['unclassified_count'] = len(self.data) - len(classified)
        metrics['classification_rate'] = (len(classified) / len(self.data)) * 100

        # Confidence distribution
        metrics['avg_confidence'] = float(classified['confidence_score'].mean())
        metrics['median_confidence'] = float(classified['confidence_score'].median())
        metrics['min_confidence'] = float(classified['confidence_score'].min())
        metrics['max_confidence'] = float(classified['confidence_score'].max())
        metrics['std_confidence'] = float(classified['confidence_score'].std())

        # Low confidence queries (< 10)
        low_conf = classified[classified['confidence_score'] < 10]
        metrics['low_confidence_count'] = len(low_conf)
        metrics['low_confidence_pct'] = (len(low_conf) / len(classified)) * 100

        # Category distribution
        l1_dist = classified['L1_category'].value_counts()
        metrics['top_l1_categories'] = l1_dist.head(5).to_dict()
        metrics['unique_topics'] = int(classified['topical_group'].nunique())

        # Commercial value
        metrics['avg_commercial_score'] = float(classified['commercial_score'].mean())
        metrics['high_value_queries'] = int(len(classified[classified['commercial_score'] >= 70]))

        self.quality_metrics = metrics

        # Print summary
        print(f"\n{'='*60}")
        print(f"DATA QUALITY SUMMARY")
        print(f"{'='*60}")
        print(f"Total Queries:        {metrics['total_queries']:,}")
        print(f"Classified:           {metrics['classified_count']:,} ({metrics['classification_rate']:.1f}%)")
        print(f"Unclassified:         {metrics['unclassified_count']:,}")
        print(f"Unique Topics:        {metrics['unique_topics']}")
        print(f"\nConfidence Scores:")
        print(f"  Average:            {metrics['avg_confidence']:.2f}")
        print(f"  Median:             {metrics['median_confidence']:.2f}")
        print(f"  Range:              {metrics['min_confidence']:.2f} - {metrics['max_confidence']:.2f}")
        print(f"  Low Confidence:     {metrics['low_confidence_count']:,} ({metrics['low_confidence_pct']:.1f}%)")
        print(f"\nTop Categories:")
        for cat, count in list(metrics['top_l1_categories'].items())[:5]:
            print(f"  {cat:20s} {count:6,} queries")
        print(f"{'='*60}\n")

        return metrics

    def perform_text_clustering(self, n_clusters=50, method='kmeans'):
        """
        Cluster queries based on text similarity

        Args:
            n_clusters: Number of clusters to create
            method: 'kmeans' or 'dbscan'
        """
        print(f"\n🔬 Performing text-based clustering ({method})...")

        if self.data is None:
            raise ValueError("No data loaded")

        # Filter to classified queries only
        classified = self.data[self.data['topical_group'] != 'Unclassified'].copy()

        print(f"   Queries to cluster: {len(classified)}")

        # Create TF-IDF vectors from query text
        print(f"   Creating TF-IDF vectors...")
        vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )

        X = vectorizer.fit_transform(classified['query'])

        # Perform clustering
        if method == 'kmeans':
            print(f"   Running K-Means (k={n_clusters})...")
            clusterer = KMeans(
                n_clusters=n_clusters,
                random_state=42,
                n_init=10
            )
        elif method == 'dbscan':
            print(f"   Running DBSCAN...")
            clusterer = DBSCAN(
                eps=0.5,
                min_samples=5,
                metric='cosine'
            )

        cluster_labels = clusterer.fit_predict(X)

        # Add cluster labels to data
        classified['cluster_id'] = cluster_labels

        # Calculate cluster quality metrics
        if len(set(cluster_labels)) > 1 and -1 not in cluster_labels:
            silhouette = silhouette_score(X, cluster_labels)
            calinski = calinski_harabasz_score(X.toarray(), cluster_labels)

            print(f"   Silhouette Score: {silhouette:.3f}")
            print(f"   Calinski-Harabasz Score: {calinski:.1f}")

        self.clusters = classified

        # Cluster summary
        cluster_sizes = classified['cluster_id'].value_counts()
        print(f"\n✅ Created {len(cluster_sizes)} clusters")
        print(f"   Avg cluster size: {cluster_sizes.mean():.1f}")
        print(f"   Largest cluster: {cluster_sizes.max()} queries")
        print(f"   Smallest cluster: {cluster_sizes.min()} queries")

        return classified

    def analyze_cluster_quality(self):
        """Analyze quality metrics for each cluster"""
        print("\n🔍 Analyzing cluster quality...")

        if self.clusters is None:
            raise ValueError("No clusters created. Run perform_text_clustering() first")

        cluster_analysis = []

        for cluster_id in sorted(self.clusters['cluster_id'].unique()):
            cluster_data = self.clusters[self.clusters['cluster_id'] == cluster_id]

            analysis = {
                'cluster_id': int(cluster_id),
                'size': int(len(cluster_data)),
                'avg_confidence': float(cluster_data['confidence_score'].mean()),
                'min_confidence': float(cluster_data['confidence_score'].min()),
                'max_confidence': float(cluster_data['confidence_score'].max()),
                'std_confidence': float(cluster_data['confidence_score'].std()),
                'avg_commercial': float(cluster_data['commercial_score'].mean()),

                # Topic diversity
                'unique_topics': int(cluster_data['topical_group'].nunique()),
                'dominant_topic': str(cluster_data['topical_group'].value_counts().index[0]),
                'dominant_topic_pct': float((cluster_data['topical_group'].value_counts().iloc[0] / len(cluster_data)) * 100),

                # Sample queries
                'sample_queries': cluster_data['query'].head(5).tolist()
            }

            # Calculate purity (how homogeneous is the topic assignment)
            analysis['purity'] = float(analysis['dominant_topic_pct'] / 100)

            # Quality flag
            if analysis['avg_confidence'] < 10:
                analysis['quality_flag'] = 'LOW_CONFIDENCE'
            elif analysis['purity'] < 0.5:
                analysis['quality_flag'] = 'LOW_PURITY'
            elif analysis['std_confidence'] > 30:
                analysis['quality_flag'] = 'HIGH_VARIANCE'
            else:
                analysis['quality_flag'] = 'OK'

            cluster_analysis.append(analysis)

        cluster_df = pd.DataFrame(cluster_analysis)

        # Sort by quality flags (issues first)
        cluster_df['flag_priority'] = cluster_df['quality_flag'].map({
            'LOW_CONFIDENCE': 1,
            'LOW_PURITY': 2,
            'HIGH_VARIANCE': 3,
            'OK': 4
        })

        cluster_df = cluster_df.sort_values(['flag_priority', 'size'], ascending=[True, False])

        self.cluster_analysis = cluster_df

        # Print summary
        print(f"\n{'='*80}")
        print(f"CLUSTER QUALITY ANALYSIS")
        print(f"{'='*80}")

        flag_counts = cluster_df['quality_flag'].value_counts()
        for flag, count in flag_counts.items():
            print(f"{flag:20s} {count:3} clusters")

        print(f"\nTop Issues (by cluster size):")
        print(f"{'='*80}")

        issues = cluster_df[cluster_df['quality_flag'] != 'OK'].head(10)
        for idx, row in issues.iterrows():
            print(f"\nCluster #{row['cluster_id']} - {row['quality_flag']}")
            print(f"  Size: {row['size']} queries")
            print(f"  Confidence: {row['avg_confidence']:.1f} (±{row['std_confidence']:.1f})")
            print(f"  Purity: {row['purity']:.1%}")
            print(f"  Dominant Topic: {row['dominant_topic']}")
            print(f"  Sample: {row['sample_queries'][0]}")

        print(f"{'='*80}\n")

        return cluster_df

    def integrate_feedback_with_clusters(self):
        """Match user feedback to clusters"""
        print("\n💬 Integrating user feedback...")

        if self.clusters is None:
            print("⚠️  No clusters available")
            return None

        if self.feedback_data is None or len(self.feedback_data) == 0:
            print("⚠️  No feedback data available")
            return None

        # Match feedback to queries
        feedback_clusters = []

        for idx, feedback in self.feedback_data.iterrows():
            query = feedback['query']

            # Find matching query in clusters
            match = self.clusters[self.clusters['query'] == query]

            if len(match) > 0:
                cluster_id = match.iloc[0]['cluster_id']
                feedback_clusters.append({
                    'cluster_id': cluster_id,
                    'query': query,
                    'feedback_type': feedback['feedback_type'],
                    'timestamp': feedback['timestamp']
                })

        if not feedback_clusters:
            print("⚠️  No feedback matches found")
            return None

        feedback_df = pd.DataFrame(feedback_clusters)

        # Calculate cluster-level feedback metrics
        cluster_feedback = feedback_df.groupby('cluster_id').agg({
            'feedback_type': lambda x: (x == 'up').sum() / len(x) * 100  # % positive
        }).rename(columns={'feedback_type': 'positive_feedback_pct'})

        cluster_feedback['feedback_count'] = feedback_df.groupby('cluster_id').size()

        print(f"✅ Matched {len(feedback_df)} feedback entries to {len(cluster_feedback)} clusters")

        return cluster_feedback

    def export_analysis(self, output_file='qa_analysis_report.json'):
        """Export complete analysis to JSON"""
        print(f"\n💾 Exporting analysis to {output_file}...")

        if self.quality_metrics is None or self.cluster_analysis is None:
            raise ValueError("Run analysis first")

        report = {
            'timestamp': datetime.now().isoformat(),
            'quality_metrics': self.quality_metrics,
            'cluster_summary': {
                'total_clusters': len(self.cluster_analysis),
                'issues_count': len(self.cluster_analysis[self.cluster_analysis['quality_flag'] != 'OK']),
                'avg_cluster_size': float(self.cluster_analysis['size'].mean()),
                'avg_confidence': float(self.cluster_analysis['avg_confidence'].mean()),
                'avg_purity': float(self.cluster_analysis['purity'].mean())
            },
            'top_issues': self.cluster_analysis[self.cluster_analysis['quality_flag'] != 'OK'].head(20).to_dict('records')
        }

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"✅ Report saved to {output_file}")

        return report


def main():
    """Main execution"""
    print("\n" + "="*80)
    print("QA CLUSTERING ANALYSIS")
    print("="*80 + "\n")

    # Initialize engine
    engine = QAClusteringEngine()

    # Load data
    engine.load_classification_data()
    engine.load_feedback_data()
    engine.load_corrections_data()

    # Run analysis
    engine.analyze_data_quality()

    # Perform clustering
    engine.perform_text_clustering(n_clusters=50, method='kmeans')

    # Analyze cluster quality
    engine.analyze_cluster_quality()

    # Integrate feedback
    engine.integrate_feedback_with_clusters()

    # Export results
    engine.export_analysis('qa_analysis_report.json')

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nNext steps:")
    print("1. Review qa_analysis_report.json")
    print("2. Check top issues in cluster analysis")
    print("3. Access dashboard at http://localhost:5001/qa-dashboard")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
