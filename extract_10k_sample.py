#!/usr/bin/env python3
"""
Extract a balanced 10,000 keyword sample from the existing 111K dataset
Maintains category distribution and brand detection support
"""

import json
import os
import random
from collections import defaultdict
from datetime import datetime


def extract_10k_sample():
    """Extract a 10K balanced sample from the 111K dataset"""

    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(script_dir, 'telecom-classification-100K.json')
    output_path = os.path.join(script_dir, 'telecom-classification-10K-sample.json')

    print("=" * 80)
    print("EXTRACTING 10K SAMPLE FROM 111K DATASET")
    print("=" * 80)

    # Load the source dataset
    print(f"\nLoading source dataset from: {source_path}")
    with open(source_path, 'r', encoding='utf-8') as f:
        source_data = json.load(f)

    # Get all keywords grouped by L1 category
    keywords_by_category = defaultdict(list)
    total_keywords = 0

    for l1 in source_data['taxonomy']['L1_categories']:
        l1_name = l1['name']
        for l2 in l1.get('L2_subcategories', []):
            for l3 in l2.get('L3_intents', []):
                for l4 in l3.get('L4_topics', []):
                    for l5 in l4.get('L5_keywords', []):
                        keywords_by_category[l1_name].append({
                            'keyword': l5,
                            'l1': l1,
                            'l2': l2,
                            'l3': l3,
                            'l4': l4
                        })
                        total_keywords += 1

    print(f"  Loaded {total_keywords:,} keywords from {len(keywords_by_category)} categories")

    # Calculate proportional sample sizes (aim for 10,000 total)
    target_total = 10000
    category_counts = {cat: len(kws) for cat, kws in keywords_by_category.items()}
    total_source = sum(category_counts.values())

    # Calculate proportional allocation
    sample_sizes = {}
    for cat, count in category_counts.items():
        proportion = count / total_source
        sample_sizes[cat] = max(10, int(proportion * target_total))  # Minimum 10 per category

    # Adjust to hit exactly 10K
    current_total = sum(sample_sizes.values())
    if current_total < target_total:
        # Add to largest categories
        sorted_cats = sorted(sample_sizes.keys(), key=lambda x: category_counts[x], reverse=True)
        diff = target_total - current_total
        for i, cat in enumerate(sorted_cats):
            if i < diff:
                sample_sizes[cat] += 1
    elif current_total > target_total:
        # Remove from largest categories
        sorted_cats = sorted(sample_sizes.keys(), key=lambda x: category_counts[x], reverse=True)
        diff = current_total - target_total
        for i, cat in enumerate(sorted_cats):
            if i < diff and sample_sizes[cat] > 10:
                sample_sizes[cat] -= 1

    print(f"\n{'Category':<30} {'Source':>10} {'Sample':>10} {'%':>8}")
    print("-" * 60)

    # Sample keywords from each category
    sampled_keywords = {}
    for cat in sorted(keywords_by_category.keys()):
        source_count = len(keywords_by_category[cat])
        sample_count = min(sample_sizes[cat], source_count)

        # Random sample
        if source_count <= sample_count:
            sampled = keywords_by_category[cat]
        else:
            sampled = random.sample(keywords_by_category[cat], sample_count)

        sampled_keywords[cat] = sampled
        pct = (sample_count / source_count) * 100 if source_count > 0 else 0
        print(f"{cat:<30} {source_count:>10,} {sample_count:>10,} {pct:>7.1f}%")

    total_sampled = sum(len(kws) for kws in sampled_keywords.values())
    print("-" * 60)
    print(f"{'TOTAL':<30} {total_source:>10,} {total_sampled:>10,}")

    # Build new taxonomy structure with sampled keywords
    print("\nBuilding sampled taxonomy structure...")

    new_taxonomy = {
        "classification_system": {
            "name": "Telecom Keyword Classification - 10K Sample",
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "source": "telecom-classification-100K.json",
            "total_keywords": total_sampled,
            "description": "10,000 keyword sample extracted from 111K dataset"
        },
        "taxonomy": {
            "L1_categories": []
        }
    }

    # Group sampled keywords back into taxonomy structure
    for cat, samples in sampled_keywords.items():
        # Group by L1 -> L2 -> L3 -> L4
        l1_data = None
        l2_map = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for sample in samples:
            l1_data = sample['l1']
            l2_name = sample['l2']['name']
            l3_id = sample['l3']['id']
            l4_topic = sample['l4']['topic']
            l2_map[l2_name][(l3_id, json.dumps(sample['l3']))][l4_topic].append(sample['keyword'])

        if l1_data:
            l1_category = {
                "id": l1_data['id'],
                "name": l1_data['name'],
                "slug": l1_data.get('slug', ''),
                "L2_subcategories": []
            }

            for l2_name, l3_data in l2_map.items():
                l2_sub = {
                    "id": f"L2_{l2_name.replace(' ', '_').upper()}",
                    "name": l2_name,
                    "slug": l2_name.lower().replace(' ', '-'),
                    "L3_intents": []
                }

                for (l3_id, l3_json), l4_data in l3_data.items():
                    l3_info = json.loads(l3_json)
                    l3_intent = {
                        "id": l3_id,
                        "intent_category": l3_info.get('intent_category', ''),
                        "intent_subcategory": l3_info.get('intent_subcategory', ''),
                        "commercial_score": l3_info.get('commercial_score', 0),
                        "funnel_stage": l3_info.get('funnel_stage', ''),
                        "conversion_probability": l3_info.get('conversion_probability', ''),
                        "L4_topics": []
                    }

                    for l4_topic, keywords in l4_data.items():
                        l4_item = {
                            "id": f"L4_{l4_topic.replace(' ', '_').upper()}",
                            "topic": l4_topic,
                            "slug": l4_topic.lower().replace(' ', '-'),
                            "L5_keywords": keywords
                        }
                        l3_intent["L4_topics"].append(l4_item)

                    l2_sub["L3_intents"].append(l3_intent)

                l1_category["L2_subcategories"].append(l2_sub)

            new_taxonomy["taxonomy"]["L1_categories"].append(l1_category)

    # Save the sampled dataset
    print(f"\nSaving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(new_taxonomy, f, indent=2)

    file_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  File size: {file_size:.2f} MB")

    print("\n" + "=" * 80)
    print("10K SAMPLE EXTRACTION COMPLETE!")
    print("=" * 80)

    return output_path


def test_sample_with_classifier(dataset_path):
    """Test the sampled dataset with the classifier"""
    from telecom_classifier import TelecomClassifier

    print("\n" + "=" * 80)
    print("TESTING CLASSIFIER WITH 10K SAMPLE DATASET")
    print("=" * 80)

    classifier = TelecomClassifier(dataset_path)
    print(f"\n  Loaded {len(classifier.keywords_index):,} keywords")

    # Test queries
    test_queries = [
        ("verizon unlimited plan", "Mobile Plans"),
        ("iphone 16 pro max", "Devices"),
        ("black friday phone deals", "Deals"),
        ("t-mobile vs att", "Comparisons"),
        ("verizon customer service number", "Customer Service"),
        ("switch from att to verizon", "Switching"),
        ("iphone trade in value", "Trade In"),
        ("5g coverage near me", "Coverage"),
        ("best phone plan los angeles", "Local"),
        ("apple watch cellular plan", "Connected Devices"),
        ("samsung galaxy s24 ultra", "Devices"),
        ("mint mobile review", "Reviews"),
        ("what is esim", "SIM"),
        ("unlock iphone verizon", "Unlocking"),
        ("international calling plan", "International"),
    ]

    print(f"\nRunning {len(test_queries)} test queries...\n")

    passed = 0
    for query, expected_l1 in test_queries:
        result = classifier.classify_text(query)
        if result:
            actual_l1 = result['classification']['L1']['name']
            is_branded = result['classification']['L2'].get('is_branded', False)
            brand_type = result['classification']['L2'].get('brand_type', '-')
            confidence = result.get('confidence_score', 0)

            status = "PASS" if actual_l1 == expected_l1 else "FAIL"
            if actual_l1 == expected_l1:
                passed += 1

            print(f"  [{status}] '{query}'")
            print(f"        Expected: {expected_l1} | Actual: {actual_l1} | Conf: {confidence:.2f}")
            print(f"        Branded: {is_branded} | Type: {brand_type}")
        else:
            print(f"  [FAIL] '{query}' - No classification")

    print(f"\n  Results: {passed}/{len(test_queries)} passed ({passed/len(test_queries)*100:.0f}%)")

    return passed == len(test_queries)


if __name__ == '__main__':
    random.seed(42)  # For reproducibility
    dataset_path = extract_10k_sample()
    test_sample_with_classifier(dataset_path)
