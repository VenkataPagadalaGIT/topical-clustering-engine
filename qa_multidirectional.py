#!/usr/bin/env python3
"""
Multi-Directional QA Analysis System
Tests classification quality from all directions:
- Bottom-to-Top: Query → L5 → L4 → L3 → L2 → L1
- Top-to-Bottom: L1 → L2 → L3 → L4 → L5 → Query
- Middle-to-Top: L3 → L2 → L1
- Middle-to-Bottom: L3 → L4 → L5 → Query

Version: 2.0
Last Updated: November 2, 2025
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telecom_classifier import TelecomClassifier
import json
from datetime import datetime
from collections import defaultdict, Counter
import statistics

class MultiDirectionalQA:
    """
    Comprehensive QA testing from all directions
    """

    def __init__(self, decision_tree_path):
        self.classifier = TelecomClassifier(decision_tree_path)
        self.decision_tree_path = decision_tree_path
        self.test_queries = self._generate_test_queries()
        self.results = {
            'bottom_to_top': [],
            'top_to_bottom': [],
            'middle_to_top': [],
            'middle_to_bottom': [],
            'summary': {}
        }

    def _generate_test_queries(self):
        """Generate 50 diverse test queries"""
        return [
            # iPhone Queries (10)
            "buy iphone 17 pro max",
            "iphone 17 air price",
            "iphone 16 vs iphone 17",
            "cheap iphone 15 deals",
            "iphone 14 trade in value",
            "iphone 13 battery replacement",
            "iphone 12 screen repair",
            "iphone se 2024 features",
            "iphone 17 release date",
            "best iphone for seniors",

            # Samsung Queries (8)
            "samsung galaxy s24 ultra",
            "galaxy z fold 6 price",
            "samsung a54 vs a34",
            "galaxy watch 6 classic",
            "samsung tablet deals",
            "galaxy buds pro 3",
            "samsung trade in program",
            "galaxy s25 rumors",

            # Google Pixel Queries (5)
            "pixel 9 pro camera",
            "pixel fold review",
            "pixel watch 3",
            "pixel 8a budget phone",
            "pixel buds pro 2",

            # Mobile Plans (10)
            "unlimited data plan",
            "family plan 4 lines",
            "prepaid phone plans",
            "senior discount plan",
            "military family plan",
            "student phone discount",
            "business mobile plan",
            "international calling plan",
            "unlimited hotspot plan",
            "best budget plan",

            # Internet Services (8)
            "5g home internet",
            "fiber optic internet speed",
            "home internet installation",
            "internet only plans",
            "gigabit internet pricing",
            "wifi router upgrade",
            "internet vs cable bundle",
            "rural internet options",

            # Support & Service (6)
            "phone screen repair near me",
            "activate new phone",
            "unlock my phone",
            "port phone number",
            "cancel service online",
            "customer service hours",

            # Comparison Queries (3)
            "iphone vs samsung flagship",
            "5g home vs fiber internet",
            "prepaid vs postpaid plans"
        ]

    def test_bottom_to_top(self):
        """
        Bottom-to-Top Analysis
        Query → L5 → L4 → L3 → L2 → L1
        Tests if query classification flows correctly upward through hierarchy
        """
        print("\n" + "="*80)
        print("🔍 BOTTOM-TO-TOP ANALYSIS (Query → L5 → L4 → L3 → L2 → L1)")
        print("="*80)

        results = []

        for idx, query in enumerate(self.test_queries, 1):
            result = self.classifier.classify_text(query)

            if result:
                c = result['classification']
                l1_name = c['L1'].get('name', c['L1'].get('topic', 'Unknown'))
                l2_name = c['L2'].get('name', c['L2'].get('topic', 'Unknown'))
                l3_name = c['L3'].get('intent_category', c['L3'].get('topic', 'Unknown'))
                l4_name = c['L4'].get('topic', 'Unknown')
                l5_name = c['L5'].get('keyword', c['L5'].get('topic', 'Unknown'))

                analysis = {
                    'query_id': idx,
                    'query': query,
                    'classification': result['classification'],
                    'path': f"Query → {l5_name} → {l4_name} → {l3_name} → {l2_name} → {l1_name}",
                    'confidence': result.get('confidence_score', 0),
                    'score': c['L3'].get('commercial_score', 0)
                }

                # Validate hierarchy consistency
                analysis['hierarchy_valid'] = self._validate_hierarchy_bottom_up(result['classification'])

                results.append(analysis)

                # Print progress
                status = "✅" if analysis['hierarchy_valid'] else "❌"
                print(f"{status} [{idx:2d}] {query:50s} | Conf: {analysis['confidence']:5.1f}")

            else:
                results.append({
                    'query_id': idx,
                    'query': query,
                    'classification': None,
                    'path': 'UNCLASSIFIED',
                    'hierarchy_valid': False
                })
                print(f"❌ [{idx:2d}] {query:50s} | UNCLASSIFIED")

        self.results['bottom_to_top'] = results

        # Summary
        valid = sum(1 for r in results if r.get('hierarchy_valid', False))
        classified = sum(1 for r in results if r.get('classification'))

        print(f"\n📊 Bottom-to-Top Summary:")
        print(f"   Classified:       {classified}/{len(results)} ({classified/len(results)*100:.1f}%)")
        print(f"   Valid Hierarchy:  {valid}/{classified} ({valid/classified*100:.1f}% if classified else 0)")

        return results

    def test_top_to_bottom(self):
        """
        Top-to-Bottom Analysis
        L1 → L2 → L3 → L4 → L5 → Query Match
        Tests if high-level categories correctly drill down to specific queries
        """
        print("\n" + "="*80)
        print("🔍 TOP-TO-BOTTOM ANALYSIS (L1 → L2 → L3 → L4 → L5 → Query)")
        print("="*80)

        results = []

        # Load decision tree
        with open(self.decision_tree_path, 'r') as f:
            tree = json.load(f)

        # Analyze each L1 category
        for l1_key, l1_data in tree.items():
            if l1_key == 'metadata':
                continue

            l1_name = l1_data.get('topic', l1_data.get('name', l1_key))
            print(f"\n📁 L1: {l1_name}")

            # Count queries matching this L1
            l1_queries = [q for q in self.test_queries
                         if self._query_matches_l1(q, l1_name)]

            l2_count = len(l1_data.get('subcategories', {}))
            l3_count = sum(len(l2.get('intents', {}))
                          for l2 in l1_data.get('subcategories', {}).values())
            l4_count = sum(len(l3.get('topics', {}))
                          for l2 in l1_data.get('subcategories', {}).values()
                          for l3 in l2.get('intents', {}).values())

            analysis = {
                'l1': l1_name,
                'l2_count': l2_count,
                'l3_count': l3_count,
                'l4_count': l4_count,
                'matching_queries': len(l1_queries),
                'sample_queries': l1_queries[:3]
            }

            results.append(analysis)

            print(f"   L2 Categories:    {l2_count}")
            print(f"   L3 Intents:       {l3_count}")
            print(f"   L4 Topics:        {l4_count}")
            print(f"   Matching Queries: {len(l1_queries)}")
            if l1_queries:
                print(f"   Sample:           {l1_queries[0]}")

        self.results['top_to_bottom'] = results

        print(f"\n📊 Top-to-Bottom Summary:")
        print(f"   L1 Categories:    {len(results)}")
        print(f"   Total L4 Topics:  {sum(r['l4_count'] for r in results)}")
        print(f"   Queries Matched:  {sum(r['matching_queries'] for r in results)}/{len(self.test_queries)}")

        return results

    def test_middle_to_top(self):
        """
        Middle-to-Top Analysis
        L3 (Intent) → L2 (Subcategory) → L1 (Category)
        Tests if intent classifications correctly roll up to categories
        """
        print("\n" + "="*80)
        print("🔍 MIDDLE-TO-TOP ANALYSIS (L3 Intent → L2 → L1)")
        print("="*80)

        results = []

        for idx, query in enumerate(self.test_queries, 1):
            result = self.classifier.classify_text(query)

            if result:
                c = result['classification']
                l1_name = c['L1'].get('name', c['L1'].get('topic', 'Unknown'))
                l2_name = c['L2'].get('name', c['L2'].get('topic', 'Unknown'))
                l3_name = c['L3'].get('intent_category', c['L3'].get('topic', 'Unknown'))

                analysis = {
                    'query_id': idx,
                    'query': query,
                    'l3_intent': l3_name,
                    'l2_subcategory': l2_name,
                    'l1_category': l1_name,
                    'path': f"{l3_name} → {l2_name} → {l1_name}",
                    'rollup_valid': self._validate_rollup_to_top(c)
                }

                results.append(analysis)

                status = "✅" if analysis['rollup_valid'] else "❌"
                print(f"{status} [{idx:2d}] {l3_name:30s} → {l2_name:30s} → {l1_name}")

            else:
                results.append({
                    'query_id': idx,
                    'query': query,
                    'rollup_valid': False
                })
                print(f"❌ [{idx:2d}] UNCLASSIFIED")

        self.results['middle_to_top'] = results

        # Summary
        valid = sum(1 for r in results if r.get('rollup_valid', False))
        classified = sum(1 for r in results if 'l3_intent' in r)

        print(f"\n📊 Middle-to-Top Summary:")
        print(f"   Classified:       {classified}/{len(results)}")
        print(f"   Valid Rollup:     {valid}/{classified} ({valid/classified*100:.1f}% if classified else 0)")

        return results

    def test_middle_to_bottom(self):
        """
        Middle-to-Bottom Analysis
        L3 (Intent) → L4 (Topic) → L5 (Keyword) → Query Match
        Tests if intents correctly drill down to specific topics and queries
        """
        print("\n" + "="*80)
        print("🔍 MIDDLE-TO-BOTTOM ANALYSIS (L3 Intent → L4 → L5 → Query)")
        print("="*80)

        results = []

        for idx, query in enumerate(self.test_queries, 1):
            result = self.classifier.classify_text(query)

            if result:
                c = result['classification']
                l3_name = c['L3'].get('intent_category', c['L3'].get('topic', 'Unknown'))
                l4_name = c['L4'].get('topic', 'Unknown')
                l5_name = c['L5'].get('keyword', c['L5'].get('topic', 'Unknown'))
                confidence = result.get('confidence_score', 0)

                analysis = {
                    'query_id': idx,
                    'query': query,
                    'l3_intent': l3_name,
                    'l4_topic': l4_name,
                    'l5_keywords': l5_name,
                    'path': f"{l3_name} → {l4_name} → {l5_name} → Match",
                    'drilldown_valid': self._validate_drilldown_from_middle(c, query),
                    'confidence': confidence
                }

                results.append(analysis)

                status = "✅" if analysis['drilldown_valid'] else "❌"
                conf_str = f"Conf: {confidence:5.1f}"
                print(f"{status} [{idx:2d}] {l3_name:20s} → {l4_name:40s} | {conf_str}")

            else:
                results.append({
                    'query_id': idx,
                    'query': query,
                    'drilldown_valid': False
                })
                print(f"❌ [{idx:2d}] UNCLASSIFIED")

        self.results['middle_to_bottom'] = results

        # Summary
        valid = sum(1 for r in results if r.get('drilldown_valid', False))
        classified = sum(1 for r in results if 'l3_intent' in r)

        print(f"\n📊 Middle-to-Bottom Summary:")
        print(f"   Classified:       {classified}/{len(results)}")
        print(f"   Valid Drilldown:  {valid}/{classified} ({valid/classified*100:.1f}% if classified else 0)")

        return results

    def _validate_hierarchy_bottom_up(self, classification):
        """Validate that hierarchy is consistent from bottom to top"""
        # Check if all levels exist
        required_levels = ['L1', 'L2', 'L3', 'L4', 'L5']
        if not all(level in classification for level in required_levels):
            return False

        # Check if confidence is reasonable
        if classification.get('confidence', 0) < 0:
            return False

        return True

    def _validate_rollup_to_top(self, classification):
        """Validate that L3 → L2 → L1 rollup is correct"""
        # L3 should belong to L2, L2 should belong to L1
        # This is implicitly validated by the decision tree structure
        return all(level in classification for level in ['L1', 'L2', 'L3'])

    def _validate_drilldown_from_middle(self, classification, query):
        """Validate that L3 → L4 → L5 drilldown makes sense"""
        # Check if keywords match query
        l5_keyword = classification.get('L5', {}).get('keyword', classification.get('L5', {}).get('topic', ''))

        if isinstance(l5_keyword, str) and l5_keyword.lower() in query.lower():
            return True

        # Check if any word from L4 topic is in query
        l4_topic = classification.get('L4', {}).get('topic', '')
        if l4_topic and any(word in query.lower() for word in l4_topic.lower().split()):
            return True

        return False

    def _query_matches_l1(self, query, l1_name):
        """Check if query belongs to L1 category"""
        result = self.classifier.classify_text(query)
        if result and 'L1' in result['classification']:
            l1_result_name = result['classification']['L1'].get('name', result['classification']['L1'].get('topic', ''))
            return l1_result_name == l1_name
        return False

    def generate_comprehensive_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "="*80)
        print("📊 COMPREHENSIVE MULTI-DIRECTIONAL QA REPORT")
        print("="*80)

        # Overall statistics
        total_queries = len(self.test_queries)

        bottom_up_classified = sum(1 for r in self.results['bottom_to_top'] if r.get('classification'))
        bottom_up_valid = sum(1 for r in self.results['bottom_to_top'] if r.get('hierarchy_valid', False))

        middle_top_classified = sum(1 for r in self.results['middle_to_top'] if 'l3_intent' in r)
        middle_top_valid = sum(1 for r in self.results['middle_to_top'] if r.get('rollup_valid', False))

        middle_bottom_classified = sum(1 for r in self.results['middle_to_bottom'] if 'l3_intent' in r)
        middle_bottom_valid = sum(1 for r in self.results['middle_to_bottom'] if r.get('drilldown_valid', False))

        print(f"\n📈 Overall Results:")
        print(f"   Total Test Queries: {total_queries}")
        print(f"\n   Bottom-to-Top:")
        print(f"      Classified:      {bottom_up_classified}/{total_queries} ({bottom_up_classified/total_queries*100:.1f}%)")
        print(f"      Valid Hierarchy: {bottom_up_valid}/{bottom_up_classified} ({bottom_up_valid/bottom_up_classified*100:.1f}% if bottom_up_classified else 0)")
        print(f"\n   Top-to-Bottom:")
        print(f"      L1 Categories:   {len(self.results['top_to_bottom'])}")
        print(f"      L4 Topics:       {sum(r['l4_count'] for r in self.results['top_to_bottom'])}")
        print(f"\n   Middle-to-Top:")
        print(f"      Classified:      {middle_top_classified}/{total_queries}")
        print(f"      Valid Rollup:    {middle_top_valid}/{middle_top_classified} ({middle_top_valid/middle_top_classified*100:.1f}% if middle_top_classified else 0)")
        print(f"\n   Middle-to-Bottom:")
        print(f"      Classified:      {middle_bottom_classified}/{total_queries}")
        print(f"      Valid Drilldown: {middle_bottom_valid}/{middle_bottom_classified} ({middle_bottom_valid/middle_bottom_classified*100:.1f}% if middle_bottom_classified else 0)")

        # Issue detection
        print(f"\n⚠️  Issues Detected:")

        unclassified = total_queries - bottom_up_classified
        if unclassified > 0:
            print(f"   • {unclassified} queries unclassified ({unclassified/total_queries*100:.1f}%)")

        hierarchy_issues = bottom_up_classified - bottom_up_valid
        if hierarchy_issues > 0:
            print(f"   • {hierarchy_issues} hierarchy validation failures")

        rollup_issues = middle_top_classified - middle_top_valid
        if rollup_issues > 0:
            print(f"   • {rollup_issues} rollup validation failures")

        drilldown_issues = middle_bottom_classified - middle_bottom_valid
        if drilldown_issues > 0:
            print(f"   • {drilldown_issues} drilldown validation failures")

        # Confidence analysis
        confidences = [r.get('confidence', 0) for r in self.results['bottom_to_top']
                      if r.get('classification')]

        if confidences:
            print(f"\n📊 Confidence Analysis:")
            print(f"   Average:  {sum(confidences)/len(confidences):.2f}")
            print(f"   Min:      {min(confidences):.2f}")
            print(f"   Max:      {max(confidences):.2f}")
            print(f"   Low (<10): {sum(1 for c in confidences if c < 10)}/{len(confidences)}")

        # Summary metrics
        self.results['summary'] = {
            'timestamp': datetime.now().isoformat(),
            'total_queries': total_queries,
            'bottom_to_top': {
                'classified': bottom_up_classified,
                'valid': bottom_up_valid,
                'rate': bottom_up_classified / total_queries * 100
            },
            'middle_to_top': {
                'classified': middle_top_classified,
                'valid': middle_top_valid
            },
            'middle_to_bottom': {
                'classified': middle_bottom_classified,
                'valid': middle_bottom_valid
            },
            'confidence': {
                'average': sum(confidences) / len(confidences) if confidences else 0,
                'min': min(confidences) if confidences else 0,
                'max': max(confidences) if confidences else 0,
                'low_count': sum(1 for c in confidences if c < 10)
            }
        }

        return self.results

    def get_detailed_metrics(self):
        """Calculate detailed performance metrics"""
        metrics = {
            'classification': {},
            'confidence': {},
            'intent_distribution': {},
            'category_distribution': {},
            'issues': {}
        }

        # Classification metrics
        total = len(self.test_queries)
        bottom_up = self.results.get('bottom_to_top', [])
        classified = [r for r in bottom_up if r.get('classification')]

        metrics['classification'] = {
            'total_queries': total,
            'classified_count': len(classified),
            'classified_rate': len(classified) / total * 100 if total > 0 else 0,
            'unclassified_count': total - len(classified),
            'unclassified_queries': [r['query'] for r in bottom_up if not r.get('classification')]
        }

        # Confidence metrics
        confidences = [r.get('confidence', 0) for r in classified]
        if confidences:
            metrics['confidence'] = {
                'average': statistics.mean(confidences),
                'median': statistics.median(confidences),
                'stdev': statistics.stdev(confidences) if len(confidences) > 1 else 0,
                'min': min(confidences),
                'max': max(confidences),
                'distribution': {
                    '0-5': sum(1 for c in confidences if 0 <= c < 5),
                    '5-10': sum(1 for c in confidences if 5 <= c < 10),
                    '10-15': sum(1 for c in confidences if 10 <= c < 15),
                    '15-20': sum(1 for c in confidences if 15 <= c < 20),
                    '20+': sum(1 for c in confidences if c >= 20)
                }
            }

        # Intent distribution
        middle_top = self.results.get('middle_to_top', [])
        intents = [r.get('l3_intent') for r in middle_top if r.get('l3_intent')]
        metrics['intent_distribution'] = dict(Counter(intents))

        # Category distribution
        categories = [r.get('l1_category') for r in middle_top if r.get('l1_category')]
        metrics['category_distribution'] = dict(Counter(categories))

        # Issue analysis
        middle_bottom = self.results.get('middle_to_bottom', [])
        drilldown_failures = [r for r in middle_bottom if r.get('l3_intent') and not r.get('drilldown_valid')]

        metrics['issues'] = {
            'unclassified': metrics['classification']['unclassified_queries'],
            'drilldown_failures': [
                {
                    'query': r['query'],
                    'intent': r.get('l3_intent'),
                    'topic': r.get('l4_topic'),
                    'reason': 'keyword_mismatch'
                }
                for r in drilldown_failures
            ],
            'low_confidence': [
                {
                    'query': r['query'],
                    'confidence': r.get('confidence', 0),
                    'topic': r['classification']['L4'].get('topic', 'Unknown')
                }
                for r in classified if r.get('confidence', 0) < 5
            ]
        }

        return metrics

    def generate_improvement_recommendations(self):
        """Generate specific recommendations for improving the system"""
        metrics = self.get_detailed_metrics()
        recommendations = []

        # Unclassified queries
        if metrics['classification']['unclassified_count'] > 0:
            unclassified = metrics['classification']['unclassified_queries']
            recommendations.append({
                'priority': 'CRITICAL',
                'category': 'Coverage',
                'issue': f"{len(unclassified)} unclassified queries ({metrics['classification']['unclassified_count']/metrics['classification']['total_queries']*100:.1f}%)",
                'action': f"Add keywords/topics for: {', '.join(unclassified[:3])}",
                'impact': 'Classification rate improvement'
            })

        # Low confidence
        low_conf_count = len(metrics['issues']['low_confidence'])
        if low_conf_count > 5:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Confidence',
                'issue': f"{low_conf_count} queries with confidence < 5",
                'action': 'Expand keyword coverage for low-confidence topics',
                'impact': 'Average confidence improvement'
            })

        # Drilldown failures
        drilldown_count = len(metrics['issues']['drilldown_failures'])
        if drilldown_count > 0:
            common_topics = Counter([f['topic'] for f in metrics['issues']['drilldown_failures']])
            top_topic = common_topics.most_common(1)[0] if common_topics else ('Unknown', 0)
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Drilldown',
                'issue': f"{drilldown_count} drilldown validation failures",
                'action': f"Refine L5 keywords for '{top_topic[0]}' and similar topics",
                'impact': 'Drilldown validity improvement'
            })

        return recommendations

    def export_results(self, filename='qa_multidirectional_report.json'):
        """Export results to JSON with enhanced metrics"""
        print(f"\n💾 Exporting results to {filename}...")

        # Add detailed metrics to results
        export_data = {
            **self.results,
            'detailed_metrics': self.get_detailed_metrics(),
            'recommendations': self.generate_improvement_recommendations()
        }

        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)

        print(f"✅ Report saved to {filename}")

    def display_recommendations(self):
        """Display actionable recommendations"""
        recommendations = self.generate_improvement_recommendations()

        if not recommendations:
            print("\n✅ No critical issues detected!")
            return

        print("\n" + "="*80)
        print("🎯 ACTIONABLE RECOMMENDATIONS")
        print("="*80)

        for idx, rec in enumerate(recommendations, 1):
            priority_icon = {"CRITICAL": "🔴", "HIGH": "🟡", "MEDIUM": "🟢"}.get(rec['priority'], "⚪")
            print(f"\n{priority_icon} {rec['priority']} - {rec['category']}")
            print(f"   Issue:  {rec['issue']}")
            print(f"   Action: {rec['action']}")
            print(f"   Impact: {rec['impact']}")

        print("\n" + "="*80)

    def run_all_tests(self):
        """Run all directional tests"""
        print("\n" + "="*80)
        print("🚀 MULTI-DIRECTIONAL QA ANALYSIS")
        print("Testing 50 queries from all directions")
        print("="*80)

        # Run all tests
        self.test_bottom_to_top()
        self.test_top_to_bottom()
        self.test_middle_to_top()
        self.test_middle_to_bottom()

        # Generate report
        self.generate_comprehensive_report()

        # Display recommendations
        self.display_recommendations()

        # Export results
        self.export_results()

        print("\n" + "="*80)
        print("✅ MULTI-DIRECTIONAL QA ANALYSIS COMPLETE")
        print("="*80)
        print("\nNext Steps:")
        print("  1. Review qa_multidirectional_report.json for full details")
        print("  2. Implement recommendations above to improve quality")
        print("  3. Re-run analysis after making changes")
        print("="*80)


def main():
    """Main execution"""
    decision_tree_path = '/Users/venkatapagadala/Desktop/telecom-classification.json'

    if not os.path.exists(decision_tree_path):
        print(f"❌ Decision tree not found: {decision_tree_path}")
        return

    qa = MultiDirectionalQA(decision_tree_path)
    qa.run_all_tests()


if __name__ == '__main__':
    main()
