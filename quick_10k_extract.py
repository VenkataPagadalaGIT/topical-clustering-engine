#!/usr/bin/env python3
"""Quick 10K keyword extractor - balanced sample from 111K dataset"""

import json
import random
from collections import defaultdict
from datetime import datetime

random.seed(42)

print("Loading 100K dataset...")
with open('telecom-classification-100K.json', 'r') as f:
    data = json.load(f)

# Collect all keywords with their paths
keywords_by_l1 = defaultdict(list)
for l1 in data['taxonomy']['L1_categories']:
    l1_name = l1['name']
    for l2 in l1.get('L2_subcategories', []):
        for l3 in l2.get('L3_intents', []):
            for l4 in l3.get('L4_topics', []):
                for kw in l4.get('L5_keywords', []):
                    keywords_by_l1[l1_name].append({
                        'keyword': kw,
                        'l2_name': l2['name'],
                        'l3_id': l3['id'],
                        'l4_topic': l4['topic']
                    })

total = sum(len(v) for v in keywords_by_l1.values())
print(f"Found {total:,} keywords across {len(keywords_by_l1)} categories")

# Calculate proportional sample per category (target 10K)
target = 10000
samples = {}
for cat, kws in keywords_by_l1.items():
    n = max(10, int((len(kws) / total) * target))
    samples[cat] = random.sample(kws, min(n, len(kws)))

sampled_total = sum(len(v) for v in samples.values())
print(f"Sampled {sampled_total:,} keywords")

# Build simplified output structure
output = {
    "classification_system": {
        "name": "Telecom Keyword Classification - 10K Sample",
        "version": "1.0",
        "created": datetime.now().isoformat(),
        "source": "telecom-classification-100K.json",
        "total_keywords": sampled_total
    },
    "taxonomy": {"L1_categories": []}
}

# Group sampled keywords back into L1 categories
for l1 in data['taxonomy']['L1_categories']:
    l1_name = l1['name']
    if l1_name not in samples:
        continue

    l1_out = {
        "id": l1['id'],
        "name": l1_name,
        "slug": l1.get('slug', ''),
        "L2_subcategories": []
    }

    # Group by L2
    by_l2 = defaultdict(list)
    for s in samples[l1_name]:
        by_l2[s['l2_name']].append(s)

    for l2_name, l2_samples in by_l2.items():
        l2_out = {
            "name": l2_name,
            "L3_intents": []
        }

        # Group by L3
        by_l3 = defaultdict(list)
        for s in l2_samples:
            by_l3[s['l3_id']].append(s)

        for l3_id, l3_samples in by_l3.items():
            l3_out = {
                "id": l3_id,
                "L4_topics": []
            }

            # Group by L4
            by_l4 = defaultdict(list)
            for s in l3_samples:
                by_l4[s['l4_topic']].append(s['keyword'])

            for l4_topic, keywords in by_l4.items():
                l3_out["L4_topics"].append({
                    "topic": l4_topic,
                    "L5_keywords": keywords
                })

            l2_out["L3_intents"].append(l3_out)

        l1_out["L2_subcategories"].append(l2_out)

    output["taxonomy"]["L1_categories"].append(l1_out)

# Save
with open('telecom-classification-10K-sample.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"Saved 10K sample with {sampled_total:,} keywords")

# Verify
with open('telecom-classification-10K-sample.json', 'r') as f:
    verify = json.load(f)
count = 0
for l1 in verify['taxonomy']['L1_categories']:
    for l2 in l1.get('L2_subcategories', []):
        for l3 in l2.get('L3_intents', []):
            for l4 in l3.get('L4_topics', []):
                count += len(l4.get('L5_keywords', []))
print(f"Verified: {count:,} keywords in output file")
