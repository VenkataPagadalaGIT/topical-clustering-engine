#!/usr/bin/env python3
"""
Brand Analysis Report Generator for Telecom Keywords
Groups keywords by branded vs non-branded and exports detailed reports
"""

import os
import json
import csv
from collections import defaultdict
from telecom_classifier import TelecomClassifier


def generate_brand_report():
    """Generate comprehensive brand analysis report"""

    # Load classifier
    script_dir = os.path.dirname(os.path.abspath(__file__))
    decision_tree_path = os.path.join(script_dir, 'telecom-classification-100K.json')

    print("=" * 80)
    print("TELECOM KEYWORDS - BRAND ANALYSIS REPORT")
    print("=" * 80)

    classifier = TelecomClassifier(decision_tree_path)
    print(f"\n✓ Loaded {len(classifier.keywords_index):,} keywords")

    # Analyze all keywords
    branded_keywords = {
        'carrier_only': [],
        'phone_only': [],
        'both': [],
    }
    non_branded_keywords = []

    # Track by carrier and phone brand
    by_carrier = defaultdict(list)
    by_phone_brand = defaultdict(list)

    # Track by category
    branded_by_category = defaultdict(lambda: {'branded': 0, 'non_branded': 0})

    print("\nAnalyzing keywords for brand detection...")

    for keyword, classification in classifier.keywords_index.items():
        brand_info = classifier._detect_brand(keyword)
        l1_category = classification['L1']['name']

        if brand_info['is_branded']:
            if brand_info['brand_type'] == 'carrier':
                branded_keywords['carrier_only'].append({
                    'keyword': keyword,
                    'carriers': brand_info['carriers'],
                    'category': l1_category
                })
                for carrier in brand_info['carriers']:
                    by_carrier[carrier].append(keyword)
            elif brand_info['brand_type'] == 'phone':
                branded_keywords['phone_only'].append({
                    'keyword': keyword,
                    'phone_brands': brand_info['phone_brands'],
                    'category': l1_category
                })
                for brand in brand_info['phone_brands']:
                    by_phone_brand[brand].append(keyword)
            else:  # both
                branded_keywords['both'].append({
                    'keyword': keyword,
                    'carriers': brand_info['carriers'],
                    'phone_brands': brand_info['phone_brands'],
                    'category': l1_category
                })
                for carrier in brand_info['carriers']:
                    by_carrier[carrier].append(keyword)
                for brand in brand_info['phone_brands']:
                    by_phone_brand[brand].append(keyword)

            branded_by_category[l1_category]['branded'] += 1
        else:
            non_branded_keywords.append({
                'keyword': keyword,
                'category': l1_category
            })
            branded_by_category[l1_category]['non_branded'] += 1

    # Calculate totals
    total_branded = (len(branded_keywords['carrier_only']) +
                    len(branded_keywords['phone_only']) +
                    len(branded_keywords['both']))
    total_non_branded = len(non_branded_keywords)
    total_keywords = total_branded + total_non_branded

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print(f"\n{'Category':<30} {'Count':>10} {'Percentage':>12}")
    print("-" * 55)

    carrier_count = len(branded_keywords['carrier_only'])
    phone_count = len(branded_keywords['phone_only'])
    both_count = len(branded_keywords['both'])

    print(f"Total Keywords               {total_keywords:>10,}")
    print(f"├── Branded Keywords         {total_branded:>10,} {(total_branded/total_keywords)*100:>10.1f}%")
    print(f"│   ├── Carrier Only         {carrier_count:>10,} {(carrier_count/total_keywords)*100:>10.1f}%")
    print(f"│   ├── Phone Brand Only     {phone_count:>10,} {(phone_count/total_keywords)*100:>10.1f}%")
    print(f"│   └── Both (Carrier+Phone) {both_count:>10,} {(both_count/total_keywords)*100:>10.1f}%")
    print(f"└── Non-Branded Keywords     {total_non_branded:>10,} {(total_non_branded/total_keywords)*100:>10.1f}%")

    # Top carriers by keyword count
    print("\n" + "=" * 80)
    print("TOP 20 CARRIERS BY KEYWORD COUNT")
    print("=" * 80)

    sorted_carriers = sorted(by_carrier.items(), key=lambda x: len(x[1]), reverse=True)[:20]
    print(f"\n{'Carrier':<25} {'Keywords':>10} {'Bar':>45}")
    print("-" * 80)

    max_carrier_count = len(sorted_carriers[0][1]) if sorted_carriers else 1
    for carrier, keywords in sorted_carriers:
        bar_length = int((len(keywords) / max_carrier_count) * 40)
        bar = "█" * bar_length
        print(f"{carrier:<25} {len(keywords):>10,} {bar}")

    # Top phone brands by keyword count
    print("\n" + "=" * 80)
    print("TOP 20 PHONE BRANDS BY KEYWORD COUNT")
    print("=" * 80)

    sorted_phones = sorted(by_phone_brand.items(), key=lambda x: len(x[1]), reverse=True)[:20]
    print(f"\n{'Phone Brand':<25} {'Keywords':>10} {'Bar':>45}")
    print("-" * 80)

    max_phone_count = len(sorted_phones[0][1]) if sorted_phones else 1
    for brand, keywords in sorted_phones:
        bar_length = int((len(keywords) / max_phone_count) * 40)
        bar = "█" * bar_length
        print(f"{brand:<25} {len(keywords):>10,} {bar}")

    # Branded vs Non-branded by Category
    print("\n" + "=" * 80)
    print("BRANDED VS NON-BRANDED BY CATEGORY")
    print("=" * 80)

    print(f"\n{'Category':<30} {'Branded':>10} {'Non-Brand':>10} {'% Branded':>12}")
    print("-" * 65)

    sorted_cats = sorted(branded_by_category.items(),
                        key=lambda x: x[1]['branded'] + x[1]['non_branded'],
                        reverse=True)

    for cat, counts in sorted_cats:
        total_cat = counts['branded'] + counts['non_branded']
        pct_branded = (counts['branded'] / total_cat * 100) if total_cat > 0 else 0
        print(f"{cat:<30} {counts['branded']:>10,} {counts['non_branded']:>10,} {pct_branded:>10.1f}%")

    # Export to CSV files
    print("\n" + "=" * 80)
    print("EXPORTING DATA TO CSV FILES")
    print("=" * 80)

    # Export branded keywords
    branded_csv_path = os.path.join(script_dir, 'branded_keywords_report.csv')
    with open(branded_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Keyword', 'Brand Type', 'Carriers', 'Phone Brands', 'Category'])

        for kw in branded_keywords['carrier_only']:
            writer.writerow([kw['keyword'], 'carrier', ', '.join(kw['carriers']), '', kw['category']])

        for kw in branded_keywords['phone_only']:
            writer.writerow([kw['keyword'], 'phone', '', ', '.join(kw['phone_brands']), kw['category']])

        for kw in branded_keywords['both']:
            writer.writerow([kw['keyword'], 'both', ', '.join(kw['carriers']), ', '.join(kw['phone_brands']), kw['category']])

    print(f"\n✓ Exported {total_branded:,} branded keywords to: branded_keywords_report.csv")

    # Export non-branded keywords
    non_branded_csv_path = os.path.join(script_dir, 'non_branded_keywords_report.csv')
    with open(non_branded_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Keyword', 'Category'])

        for kw in non_branded_keywords:
            writer.writerow([kw['keyword'], kw['category']])

    print(f"✓ Exported {total_non_branded:,} non-branded keywords to: non_branded_keywords_report.csv")

    # Export summary by carrier
    carrier_summary_path = os.path.join(script_dir, 'carrier_keyword_summary.csv')
    with open(carrier_summary_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Carrier', 'Keyword Count', 'Sample Keywords'])

        for carrier, keywords in sorted_carriers:
            samples = ', '.join(keywords[:5])
            writer.writerow([carrier, len(keywords), samples])

    print(f"✓ Exported carrier summary to: carrier_keyword_summary.csv")

    # Export summary by phone brand
    phone_summary_path = os.path.join(script_dir, 'phone_brand_keyword_summary.csv')
    with open(phone_summary_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Phone Brand', 'Keyword Count', 'Sample Keywords'])

        for brand, keywords in sorted_phones:
            samples = ', '.join(keywords[:5])
            writer.writerow([brand, len(keywords), samples])

    print(f"✓ Exported phone brand summary to: phone_brand_keyword_summary.csv")

    # Export category breakdown
    category_breakdown_path = os.path.join(script_dir, 'category_brand_breakdown.csv')
    with open(category_breakdown_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Category', 'Branded Count', 'Non-Branded Count', 'Total', 'Percent Branded'])

        for cat, counts in sorted_cats:
            total_cat = counts['branded'] + counts['non_branded']
            pct_branded = (counts['branded'] / total_cat * 100) if total_cat > 0 else 0
            writer.writerow([cat, counts['branded'], counts['non_branded'], total_cat, f"{pct_branded:.1f}%"])

    print(f"✓ Exported category breakdown to: category_brand_breakdown.csv")

    # Export JSON summary
    json_summary_path = os.path.join(script_dir, 'brand_analysis_summary.json')
    summary = {
        'total_keywords': total_keywords,
        'branded_count': total_branded,
        'non_branded_count': total_non_branded,
        'branded_percentage': round((total_branded / total_keywords) * 100, 2),
        'breakdown': {
            'carrier_only': len(branded_keywords['carrier_only']),
            'phone_only': len(branded_keywords['phone_only']),
            'both': len(branded_keywords['both'])
        },
        'top_carriers': {carrier: len(kws) for carrier, kws in sorted_carriers[:10]},
        'top_phone_brands': {brand: len(kws) for brand, kws in sorted_phones[:10]},
        'by_category': {cat: counts for cat, counts in sorted_cats}
    }

    with open(json_summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print(f"✓ Exported JSON summary to: brand_analysis_summary.json")

    print("\n" + "=" * 80)
    print("REPORT GENERATION COMPLETE")
    print("=" * 80)

    return summary


def show_sample_classifications():
    """Show sample classifications with brand detection"""

    script_dir = os.path.dirname(os.path.abspath(__file__))
    decision_tree_path = os.path.join(script_dir, 'telecom-classification-100K.json')

    classifier = TelecomClassifier(decision_tree_path)

    print("\n" + "=" * 80)
    print("SAMPLE CLASSIFICATIONS WITH BRAND DETECTION")
    print("=" * 80)

    test_queries = [
        # Branded carrier queries
        "verizon unlimited plan",
        "t-mobile family plan",
        "att prepaid options",
        "verizon customer service number",
        "switch from att to verizon",

        # Branded phone queries
        "iphone 16 pro max",
        "samsung galaxy s24 ultra",
        "google pixel 9 pro",

        # Both carrier and phone
        "verizon iphone 15 deal",
        "t-mobile samsung trade in",
        "att iphone upgrade",

        # Non-branded queries
        "best unlimited plan",
        "cheap phone plan",
        "5g coverage near me",
        "family plan comparison",
        "phone trade in value",
    ]

    print(f"\n{'Query':<40} {'Category':<20} {'Branded?':<10} {'Brand Type':<12} {'Brands Detected'}")
    print("-" * 120)

    for query in test_queries:
        result = classifier.classify_text(query)
        if result:
            l1 = result['classification']['L1']['name']
            l2 = result['classification']['L2']
            is_branded = "Yes" if l2.get('is_branded') else "No"
            brand_type = l2.get('brand_type') or '-'

            brands = []
            if l2.get('detected_carriers'):
                brands.extend(l2['detected_carriers'][:2])
            if l2.get('detected_phone_brands'):
                brands.extend(l2['detected_phone_brands'][:2])
            brands_str = ', '.join(brands) if brands else '-'

            print(f"{query:<40} {l1:<20} {is_branded:<10} {brand_type:<12} {brands_str}")
        else:
            print(f"{query:<40} {'No classification':<20}")


if __name__ == '__main__':
    summary = generate_brand_report()
    show_sample_classifications()
