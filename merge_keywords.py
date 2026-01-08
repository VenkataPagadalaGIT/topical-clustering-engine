#!/usr/bin/env python3
"""
Smart Keyword Merger
Merges new keywords into the existing 111K dataset without duplicates
"""

import json
import os
from collections import defaultdict
from datetime import datetime


def merge_keywords():
    """Merge new keywords into the core 111K dataset"""

    script_dir = os.path.dirname(os.path.abspath(__file__))
    core_path = os.path.join(script_dir, 'telecom-classification-100K.json')

    print("=" * 80)
    print("SMART KEYWORD MERGER")
    print("=" * 80)

    # Load the core dataset
    print(f"\nLoading core dataset...")
    with open(core_path, 'r', encoding='utf-8') as f:
        core_data = json.load(f)

    # Extract existing keywords into a set
    existing_keywords = set()
    for l1 in core_data['taxonomy']['L1_categories']:
        for l2 in l1.get('L2_subcategories', []):
            for l3 in l2.get('L3_intents', []):
                for l4 in l3.get('L4_topics', []):
                    for l5 in l4.get('L5_keywords', []):
                        kw = l5.get('keyword', l5) if isinstance(l5, dict) else l5
                        existing_keywords.add(kw.lower().strip())

    print(f"  Existing keywords: {len(existing_keywords):,}")

    # Define NEW keywords to add (not in existing dataset)
    # These are high-value keywords based on current trends
    new_keywords_by_category = {
        'Mobile Plans': [
            # 2025 specific
            'best phone plan 2025', 'cheapest unlimited plan 2025', 'best prepaid plan 2025',
            'best family plan 2025', 'best senior plan 2025', 'best student plan 2025',
            # AI/Tech terms
            'ai phone plan', 'satellite phone plan', 'starlink phone plan',
            # Specific price points
            'unlimited plan $15', 'unlimited plan $20', 'unlimited plan $25',
            'family plan $100', 'family plan $150', 'family plan $200',
            # Very specific searches
            'no credit check phone plan', 'phone plan no deposit', 'instant activation phone plan',
        ],
        'Devices': [
            # 2025 devices
            'iphone 17', 'iphone 17 pro', 'iphone 17 pro max', 'iphone 17 ultra',
            'galaxy s25', 'galaxy s25 ultra', 'galaxy s25 plus', 'galaxy s25 fe',
            'pixel 10', 'pixel 10 pro', 'pixel 10 xl',
            'galaxy z flip 7', 'galaxy z fold 7',
            # AI phones
            'ai phone', 'best ai phone', 'phone with ai', 'ai camera phone',
            # Foldables
            'best foldable phone 2025', 'cheapest foldable phone', 'foldable phone deals',
            # Satellite
            'satellite phone', 'phone with satellite', 'emergency satellite phone',
        ],
        'Deals': [
            # 2025 deals
            'phone deals 2025', 'best phone deals january 2025', 'super bowl phone deals 2025',
            'tax refund phone deals 2025', 'back to school phone deals 2025',
            # BOGO deals
            'bogo phone deal', 'buy one get one phone', 'bogo iphone', 'bogo samsung',
            # Trade-in deals
            'best trade in deal 2025', 'highest trade in value', 'trade in iphone 15',
        ],
        'Coverage': [
            # Satellite coverage
            'satellite coverage', 'starlink mobile coverage', 'satellite phone coverage',
            # 5G specific
            '5g ultra wideband coverage', '5g mmwave coverage', 'c-band 5g coverage',
            # Rural
            'best rural coverage', 'rural phone coverage', 'farm phone coverage',
        ],
        'Connected Devices': [
            # 2025 devices
            'apple watch 11 plan', 'apple watch ultra 3 plan', 'galaxy watch 7 plan',
            'pixel watch 3 plan', 'vision pro cellular', 'meta quest cellular',
            # IoT
            'iot cellular plan', 'pet tracker plan', 'car tracker plan', 'kid tracker plan',
        ],
        'Features': [
            # AI features
            'ai call screening', 'ai voicemail transcription', 'ai spam blocking',
            # Satellite
            'satellite messaging', 'emergency sos satellite', 'satellite texting',
            # Privacy
            'privacy focused phone plan', 'encrypted calling plan', 'secure phone plan',
        ],
        'Comparisons': [
            # 2025 comparisons
            'iphone 16 vs iphone 17', 'galaxy s24 vs s25', 'pixel 9 vs pixel 10',
            'iphone 17 vs galaxy s25', 'visible vs mint mobile 2025',
            # Feature comparisons
            'best 5g coverage vs best price', 'prepaid vs postpaid 2025',
        ],
        'FAQ': [
            # AI questions
            'what is ai phone', 'how does ai calling work', 'is ai spam blocking free',
            # Satellite questions
            'how does satellite texting work', 'is satellite calling free',
            'what phones have satellite', 'do i need satellite on my phone',
            # eSIM questions
            'can i have 2 esim', 'how many esim can i have', 'esim vs physical sim 2025',
        ],
    }

    # Count new keywords
    new_count = 0
    added_count = 0

    for category, keywords in new_keywords_by_category.items():
        for kw in keywords:
            kw_lower = kw.lower().strip()
            new_count += 1
            if kw_lower not in existing_keywords:
                # Find the L1 category
                for l1 in core_data['taxonomy']['L1_categories']:
                    if l1['name'] == category:
                        # Add to first L2/L3/L4 (or create new)
                        if l1.get('L2_subcategories'):
                            l2 = l1['L2_subcategories'][0]
                            if l2.get('L3_intents'):
                                l3 = l2['L3_intents'][0]
                                if l3.get('L4_topics'):
                                    l4 = l3['L4_topics'][0]
                                    # Add keyword
                                    l4['L5_keywords'].append({
                                        'keyword': kw,
                                        'search_volume': 1000,
                                        'difficulty': 50,
                                        'added': '2025-01'
                                    })
                                    existing_keywords.add(kw_lower)
                                    added_count += 1
                        break

    print(f"  New keywords proposed: {new_count}")
    print(f"  Keywords added (non-duplicates): {added_count}")
    print(f"  Total keywords now: {len(existing_keywords):,}")

    # Update metadata
    core_data['classification_system']['total_keywords'] = len(existing_keywords)
    core_data['classification_system']['last_updated'] = datetime.now().isoformat()
    core_data['classification_system']['version'] = '2.0'

    # Save updated dataset
    print(f"\nSaving updated dataset...")
    with open(core_path, 'w', encoding='utf-8') as f:
        json.dump(core_data, f, indent=2)

    file_size = os.path.getsize(core_path) / (1024 * 1024)
    print(f"  File size: {file_size:.2f} MB")

    print("\n" + "=" * 80)
    print("MERGE COMPLETE!")
    print("=" * 80)

    # Test the merged dataset
    print("\nTesting merged dataset...")
    from telecom_classifier import TelecomClassifier
    classifier = TelecomClassifier(core_path)
    print(f"  Classifier loaded: {len(classifier.keywords_index):,} keywords")

    # Test some new keywords
    test_queries = [
        'iphone 17 pro max',
        'galaxy s25 ultra',
        'ai phone',
        'satellite phone plan',
        'bogo phone deal',
    ]

    print("\nTesting new keywords:")
    for query in test_queries:
        result = classifier.classify_text(query)
        if result:
            l1 = result['classification']['L1']['name']
            branded = result['classification']['L2'].get('is_branded', False)
            print(f"  '{query}' -> {l1} (Branded: {branded})")
        else:
            print(f"  '{query}' -> No match (will use fallback)")


if __name__ == '__main__':
    merge_keywords()
