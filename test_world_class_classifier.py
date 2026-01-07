#!/usr/bin/env python3
"""
Test World-Class iPhone Classifier
Validate that ALL iPhone models now classify correctly
"""

import sys
sys.path.append('/Users/venkatapagadala/Desktop')

from telecom_classifier import TelecomClassifier

def test_iphone_classifications():
    """Test comprehensive iPhone classification coverage"""

    print("=" * 80)
    print("🧪 TESTING WORLD-CLASS iPHONE CLASSIFIER")
    print("=" * 80)
    print()

    # Initialize classifier with expanded tree
    classifier = TelecomClassifier('/Users/venkatapagadala/Desktop/telecom-classification.json')

    # Test cases covering ALL scenarios user requested
    test_queries = [
        # User's original failing query
        ("iphone 17 vs S24", "iPhone 17 Pro Max", "Comparative"),

        # Current generation 2025
        ("iphone 17 pro max price", "iPhone 17 Pro Max", "Transactional"),
        ("buy iphone 17 pro", "iPhone 17 Pro", "Transactional"),
        ("iphone 17 air review", "iPhone 17 Air", "Comparative"),
        ("iphone 17 specs", "iPhone 17", "Informational"),
        ("iphone 17 vs iphone 16", "iPhone 17", "Comparative"),

        # iPhone Air (new ultra-thin model)
        ("iphone air features", "iPhone 17 Air", "Informational"),
        ("buy iphone air", "iPhone 17 Air", "Transactional"),
        ("iphone air thickness", "iPhone 17 Air", "Informational"),

        # 2024 models
        ("iphone 16 pro max", "iPhone 16 Pro Max", "Transactional"),
        ("iphone 16 colors", "iPhone 16", "Informational"),
        ("iphone 16e price", "iPhone 16e", "Transactional"),

        # 2023 models
        ("iphone 15 pro max vs iphone 15 pro", "iPhone 15 Pro Max", "Comparative"),
        ("iphone 15 plus review", "iPhone 15 Plus", "Comparative"),

        # 2022 models
        ("iphone 14 pro max battery life", "iPhone 14 Pro Max", "Informational"),
        ("buy iphone 14", "iPhone 14", "Transactional"),

        # Older models
        ("iphone 13 mini in stock", "iPhone 13 Mini", "Local"),
        ("iphone 12 trade in value", "iPhone 12", "Transactional"),
        ("iphone 11 camera quality", "iPhone 11", "Informational"),

        # Special editions
        ("iphone se 3rd gen price", "iPhone SE", "Transactional"),
        ("iphone se vs iphone 13", "iPhone SE", "Comparative"),

        # X series
        ("iphone xs max screen repair", "iPhone XS Max", "Navigational"),
        ("iphone xr colors", "iPhone XR", "Informational"),

        # Legacy models
        ("iphone 8 plus battery replacement", "iPhone 8 Plus", "Navigational"),
        ("iphone 7 still worth it", "iPhone 7", "Informational"),
        ("iphone 6s specs", "iPhone 6S", "Informational"),

        # Comparison queries
        ("iphone 17 pro max vs iphone air", "iPhone 17 Pro Max", "Comparative"),
        ("iphone vs samsung", "iPhone", "Comparative"),
        ("iphone 16 pro vs pixel 9 pro", "iPhone 16 Pro", "Comparative"),

        # Purchase intent variations
        ("where to buy iphone 17", "iPhone 17", "Local"),
        ("iphone 17 deals", "iPhone 17", "Transactional"),
        ("order iphone 17 pro max", "iPhone 17 Pro Max", "Transactional"),
        ("iphone 17 pre-order", "iPhone 17", "Transactional"),

        # Support/Navigation
        ("iphone 15 setup guide", "iPhone 15", "Navigational"),
        ("iphone 16 activation", "iPhone 16", "Navigational"),
        ("how to transfer data to iphone 17", "iPhone 17", "Navigational"),

        # Local intent
        ("iphone 17 pro max near me", "iPhone 17 Pro Max", "Local"),
        ("iphone 16 in stock near me", "iPhone 16", "Local"),
        ("apple store iphone 17", "iPhone 17", "Local"),
    ]

    print(f"Testing {len(test_queries)} queries...\n")

    results = {
        "total": len(test_queries),
        "correct_model": 0,
        "correct_intent": 0,
        "high_confidence": 0,
        "perfect": 0,
        "failed": []
    }

    for i, (query, expected_model_contains, expected_intent) in enumerate(test_queries, 1):
        result = classifier.classify_text(query)

        # Check if result contains expected model
        topical_group = result.get('topical_group', '')
        l3_intent = result.get('L3_intent', '')
        confidence = result.get('confidence_score', 0)

        model_match = expected_model_contains.lower() in topical_group.lower()
        intent_match = expected_intent in l3_intent
        high_conf = confidence >= 50

        if model_match:
            results['correct_model'] += 1
        if intent_match:
            results['correct_intent'] += 1
        if high_conf:
            results['high_confidence'] += 1
        if model_match and intent_match and high_conf:
            results['perfect'] += 1

        # Status indicator
        if model_match and intent_match and high_conf:
            status = "✅ PERFECT"
        elif model_match and intent_match:
            status = "✓ GOOD"
        elif model_match:
            status = "~ PARTIAL"
        else:
            status = "❌ FAILED"
            results['failed'].append({
                "query": query,
                "expected": expected_model_contains,
                "got": topical_group,
                "confidence": confidence
            })

        print(f"{i:2d}. {status} | Query: {query:<40} | Got: {topical_group:<50} | Conf: {confidence:>5.1f} | Intent: {l3_intent}")

    # Summary
    print()
    print("=" * 80)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 80)
    print(f"Total Queries Tested:       {results['total']}")
    print(f"Correct Model Detection:    {results['correct_model']}/{results['total']} ({results['correct_model']/results['total']*100:.1f}%)")
    print(f"Correct Intent Detection:   {results['correct_intent']}/{results['total']} ({results['correct_intent']/results['total']*100:.1f}%)")
    print(f"High Confidence (≥50):      {results['high_confidence']}/{results['total']} ({results['high_confidence']/results['total']*100:.1f}%)")
    print(f"Perfect Classifications:    {results['perfect']}/{results['total']} ({results['perfect']/results['total']*100:.1f}%)")
    print()

    if results['failed']:
        print(f"⚠️  {len(results['failed'])} queries need attention:")
        for fail in results['failed']:
            print(f"   • '{fail['query']}' → Expected: {fail['expected']}, Got: {fail['got']} (conf: {fail['confidence']:.1f})")
        print()

    # Overall grade
    perfect_rate = results['perfect'] / results['total']
    if perfect_rate >= 0.95:
        grade = "🏆 WORLD-CLASS"
    elif perfect_rate >= 0.85:
        grade = "🥇 EXCELLENT"
    elif perfect_rate >= 0.70:
        grade = "🥈 GOOD"
    elif perfect_rate >= 0.50:
        grade = "🥉 FAIR"
    else:
        grade = "⚠️  NEEDS IMPROVEMENT"

    print(f"Overall Grade: {grade}")
    print("=" * 80)
    print()

    return results

if __name__ == "__main__":
    test_iphone_classifications()
