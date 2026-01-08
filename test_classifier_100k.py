#!/usr/bin/env python3
"""
Comprehensive Test Suite for Telecom Classifier with 100K Keywords Dataset
Tests classification accuracy across multiple categories
"""

import os
import json
import time
from telecom_classifier import TelecomClassifier

def run_tests():
    """Run comprehensive classification tests"""

    # Load classifier with 100K dataset
    script_dir = os.path.dirname(os.path.abspath(__file__))
    decision_tree_path = os.path.join(script_dir, 'telecom-classification-100K.json')

    print("=" * 80)
    print("TELECOM CLASSIFIER - 100K DATASET TEST SUITE")
    print("=" * 80)

    start_time = time.time()
    classifier = TelecomClassifier(decision_tree_path)
    load_time = time.time() - start_time

    print(f"\n✓ Loaded {len(classifier.keywords_index):,} keywords in {load_time:.2f}s")
    print("-" * 80)

    # Define test cases with expected categories
    test_cases = [
        # 1-5: Carrier/Plan queries
        {"query": "verizon unlimited plan", "expected_l1": "Mobile Plans", "category": "Carrier Plans"},
        {"query": "t-mobile family plan", "expected_l1": "Family Plans", "category": "Family Plans"},
        {"query": "att prepaid plan", "expected_l1": "Mobile Plans", "category": "Prepaid Plans"},
        {"query": "mint mobile review", "expected_l1": "Reviews", "category": "Carrier Reviews"},
        {"query": "switch from att to verizon", "expected_l1": "Switching", "category": "Carrier Switch"},

        # 6-10: Device queries
        {"query": "iphone 16 pro max", "expected_l1": "Devices", "category": "iPhone"},
        {"query": "samsung galaxy s24 ultra", "expected_l1": "Devices", "category": "Samsung"},
        {"query": "google pixel 9 pro", "expected_l1": "Devices", "category": "Pixel"},
        {"query": "cheap android phone", "expected_l1": "Devices", "category": "Budget Phones"},
        {"query": "best phone 2025", "expected_l1": "Devices", "category": "Best Phones"},

        # 11-15: Deal/Price queries
        {"query": "black friday phone deals", "expected_l1": "Deals", "category": "Seasonal Deals"},
        {"query": "iphone trade in value", "expected_l1": "Trade In", "category": "Trade In"},
        {"query": "phone plan under $30", "expected_l1": "Pricing", "category": "Price Search"},
        {"query": "verizon cyber monday deals", "expected_l1": "Deals", "category": "Carrier Deals"},
        {"query": "best budget phone plan", "expected_l1": "Mobile Plans", "category": "Budget Plans"},

        # 16-20: Coverage/Technical queries
        {"query": "5g coverage near me", "expected_l1": "Coverage", "category": "5G Coverage"},
        {"query": "t-mobile coverage map", "expected_l1": "Coverage", "category": "Coverage Maps"},
        {"query": "what is esim", "expected_l1": "SIM", "category": "SIM Cards"},
        {"query": "unlock iphone verizon", "expected_l1": "Unlocking", "category": "Phone Unlock"},
        {"query": "byod compatibility check", "expected_l1": "BYOD", "category": "Compatibility"},

        # 21-25: Support/Service queries
        {"query": "verizon customer service number", "expected_l1": "Customer Service", "category": "Carrier Support"},
        {"query": "how to activate new phone", "expected_l1": "Activation", "category": "Phone Activation"},
        {"query": "phone not connecting to network", "expected_l1": "Support", "category": "Troubleshooting"},
        {"query": "verizon pay my bill", "expected_l1": "Billing", "category": "Payments"},
        {"query": "verizon store near me", "expected_l1": "Retail", "category": "Carrier Stores"},

        # 26-30: Comparison queries
        {"query": "verizon vs att coverage", "expected_l1": "Comparisons", "category": "Carrier Comparisons"},
        {"query": "iphone vs samsung", "expected_l1": "Devices", "category": "Phone Comparisons"},
        {"query": "prepaid vs postpaid", "expected_l1": "Comparisons", "category": "Plan Comparisons"},
        {"query": "best mvno on verizon network", "expected_l1": "MVNO", "category": "Network MVNOs"},
        {"query": "t-mobile vs visible", "expected_l1": "Comparisons", "category": "Carrier Comparisons"},

        # 31-35: Feature/Perk queries
        {"query": "unlimited hotspot plan", "expected_l1": "Mobile Plans", "category": "Feature Plans"},
        {"query": "netflix included phone plan", "expected_l1": "Perks", "category": "Streaming Perks"},
        {"query": "international calling plan", "expected_l1": "International", "category": "Calling"},
        {"query": "senior cell phone plan", "expected_l1": "Mobile Plans", "category": "Demographic Plans"},
        {"query": "military discount phone plan", "expected_l1": "Mobile Plans", "category": "Demographic Plans"},

        # 36-40: Local/Location queries
        {"query": "best phone plan los angeles", "expected_l1": "Local", "category": "City Plans"},
        {"query": "cell phone stores chicago", "expected_l1": "Local", "category": "City Stores"},
        {"query": "internet providers new york", "expected_l1": "Local", "category": "City Coverage"},
        {"query": "5g coverage miami", "expected_l1": "Local", "category": "5G Coverage"},
        {"query": "verizon store seattle", "expected_l1": "Local", "category": "Carrier Stores"},

        # 41-45: Connected Devices queries
        {"query": "apple watch cellular plan", "expected_l1": "Connected Devices", "category": "Device Plans"},
        {"query": "ipad data plan", "expected_l1": "Connected Devices", "category": "Data Plans"},
        {"query": "smartwatch plan verizon", "expected_l1": "Connected Devices", "category": "Carrier Plans"},
        {"query": "galaxy watch plan", "expected_l1": "Connected Devices", "category": "Device Plans"},
        {"query": "tablet cellular plan", "expected_l1": "Connected Devices", "category": "Data Plans"},

        # 46-50: Accessories queries
        {"query": "iphone 16 case", "expected_l1": "Accessories", "category": "Cases"},
        {"query": "wireless charger samsung", "expected_l1": "Accessories", "category": "Chargers"},
        {"query": "screen protector pixel 9", "expected_l1": "Accessories", "category": "Screen Protectors"},
        {"query": "best airpods alternative", "expected_l1": "Accessories", "category": "Earbuds"},
        {"query": "magsafe charger", "expected_l1": "Accessories", "category": "Chargers"},
    ]

    # Run tests
    print(f"\nRunning {len(test_cases)} test cases...\n")

    results = {
        'passed': 0,
        'failed': 0,
        'partial': 0,
        'details': []
    }

    for i, test in enumerate(test_cases, 1):
        query = test['query']
        expected_l1 = test['expected_l1']

        # Classify
        start = time.time()
        result = classifier.classify_text(query)
        elapsed = (time.time() - start) * 1000  # ms

        if result:
            actual_l1 = result['classification']['L1']['name']
            confidence = result['confidence_score']
            match_type = result.get('match_type', 'unknown')

            # Check if L1 matches
            passed = actual_l1 == expected_l1

            status = "✓ PASS" if passed else "✗ FAIL"
            if not passed and confidence >= 0.5:
                status = "◐ PARTIAL"
                results['partial'] += 1
            elif passed:
                results['passed'] += 1
            else:
                results['failed'] += 1

            print(f"Test {i:2d}: {status}")
            print(f"         Query: {query}")
            print(f"         Expected: {expected_l1} | Actual: {actual_l1}")
            print(f"         Confidence: {confidence:.2f} | Match: {match_type} | Time: {elapsed:.1f}ms")
            print()

            results['details'].append({
                'test_num': i,
                'query': query,
                'expected': expected_l1,
                'actual': actual_l1,
                'confidence': confidence,
                'passed': passed,
                'time_ms': elapsed
            })
        else:
            results['failed'] += 1
            print(f"Test {i:2d}: ✗ FAIL (No classification)")
            print(f"         Query: {query}")
            print(f"         Expected: {expected_l1}")
            print()

            results['details'].append({
                'test_num': i,
                'query': query,
                'expected': expected_l1,
                'actual': None,
                'confidence': 0,
                'passed': False,
                'time_ms': 0
            })

    # Print summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    total = len(test_cases)
    pass_rate = (results['passed'] / total) * 100

    print(f"\n  Total Tests:    {total}")
    print(f"  ✓ Passed:       {results['passed']} ({(results['passed']/total)*100:.1f}%)")
    print(f"  ◐ Partial:      {results['partial']} ({(results['partial']/total)*100:.1f}%)")
    print(f"  ✗ Failed:       {results['failed']} ({(results['failed']/total)*100:.1f}%)")
    print(f"\n  Overall Accuracy: {pass_rate:.1f}%")

    # Performance stats
    times = [d['time_ms'] for d in results['details'] if d['time_ms'] > 0]
    if times:
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)
        print(f"\n  Avg Response Time: {avg_time:.1f}ms")
        print(f"  Min Response Time: {min_time:.1f}ms")
        print(f"  Max Response Time: {max_time:.1f}ms")

    print("\n" + "=" * 80)

    return results


def test_specific_categories():
    """Test specific category coverage"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    decision_tree_path = os.path.join(script_dir, 'telecom-classification-100K.json')

    classifier = TelecomClassifier(decision_tree_path)

    print("\n" + "=" * 80)
    print("CATEGORY COVERAGE TEST")
    print("=" * 80)

    # Count keywords by L1 category
    category_counts = {}
    for keyword, data in classifier.keywords_index.items():
        l1_name = data['L1']['name']
        category_counts[l1_name] = category_counts.get(l1_name, 0) + 1

    print(f"\nKeywords by Category (Top 20):\n")
    sorted_cats = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:20]

    for cat, count in sorted_cats:
        bar = "█" * min(50, count // 500)
        print(f"  {cat:25s} {count:6,d} {bar}")

    print(f"\n  Total Categories: {len(category_counts)}")
    print(f"  Total Keywords:   {len(classifier.keywords_index):,}")


if __name__ == '__main__':
    results = run_tests()
    test_specific_categories()
