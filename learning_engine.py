#!/usr/bin/env python3
"""
Adaptive Learning Engine for Telecom Classifier
Learns new patterns and updates decision tree automatically
"""

import json
import re
from collections import defaultdict, Counter
from datetime import datetime
import os


class LearningEngine:
    """Learns from unclassified queries and updates the knowledge base"""

    def __init__(self, decision_tree_path):
        self.decision_tree_path = decision_tree_path
        self.learned_patterns = defaultdict(list)
        self.new_entities = {
            'devices': set(),
            'plans': set(),
            'services': set(),
            'features': set()
        }
        self.pattern_confidence = defaultdict(int)

    def analyze_unclassified(self, query: str) -> dict:
        """Analyze an unclassified query to extract learnable patterns"""
        query_lower = query.lower()
        learned = {}

        # Comprehensive device patterns for all major brands and models
        device_patterns = {
            # iPhone - all variants (numbers, Plus, Pro, Pro Max, Mini, Air, Ultra, SE)
            'iphone': r'\biphone\s+(\d+(?:\s*(?:plus|pro(?:\s+max)?|mini|air|ultra))?|se(?:\s+\d+(?:st|nd|rd)?)?|(?:plus|pro(?:\s+max)?|mini|air|ultra))',

            # Samsung Galaxy S series (S1-S30 with variants)
            'samsung_galaxy_s': r'\bsamsung\s+(?:galaxy\s+)?s(\d+)(?:\s+(ultra|plus|\+|pro|fe|edge|lite))*',

            # Samsung Galaxy A series (A1-A99 with variants)
            'samsung_galaxy_a': r'\bsamsung\s+(?:galaxy\s+)?a(\d+)(?:\s+(ultra|plus|\+|pro|5g|4g|lite))*',

            # Samsung Galaxy Note series
            'samsung_galaxy_note': r'\bsamsung\s+(?:galaxy\s+)?note\s*(\d+)(?:\s+(ultra|plus|\+|pro))*',

            # Samsung Galaxy Z series (Fold, Flip)
            'samsung_galaxy_z': r'\bsamsung\s+(?:galaxy\s+)?z\s*(fold|flip)(?:\s+(\d+))?',

            # Samsung Galaxy M series
            'samsung_galaxy_m': r'\bsamsung\s+(?:galaxy\s+)?m(\d+)(?:\s+(ultra|plus|\+|pro|5g))*',

            # Google Pixel (all versions)
            'pixel': r'\bpixel\s+(\d+(?:\s*(?:pro|xl|a))?)',

            # OnePlus (all versions with Pro, T variants)
            'oneplus': r'\boneplus\s+(\d+(?:\s*(?:pro|t|r))?)',

            # Xiaomi/Mi/Redmi
            'xiaomi': r'\b(?:xiaomi|mi|redmi)\s+(?:note\s+)?(\d+(?:\s*(?:pro|ultra|lite|s|t))?)',

            # Oppo
            'oppo': r'\boppo\s+(find\s+[xn]\d+|reno\s*\d+|a\d+)(?:\s+(pro|ultra|lite))*',

            # Vivo
            'vivo': r'\bvivo\s+([vxy]\d+)(?:\s+(pro|ultra|lite))*',

            # Motorola
            'motorola': r'\b(?:motorola|moto)\s+(?:edge|g|e|z)(?:\s+)?(\d+)(?:\s+(plus|\+|pro|ultra))*',

            # LG
            'lg': r'\blg\s+(g\d+|v\d+|wing|velvet)(?:\s+(thinq|pro))*',

            # Sony Xperia
            'sony_xperia': r'\bsony\s+xperia\s+(\d+|[ivx]+)(?:\s+(pro|ultra|compact))*',

            # Nokia
            'nokia': r'\bnokia\s+(\d+(?:\.\d+)?)(?:\s+(pro|plus|\+))*',

            # Huawei
            'huawei': r'\bhuawei\s+(p\d+|mate\s*\d+)(?:\s+(pro|ultra|lite))*',
        }

        # Track brand for better L2 categorization
        detected_brand = None

        for brand, pattern in device_patterns.items():
            matches = re.findall(pattern, query_lower, re.IGNORECASE)
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        # Filter out empty strings from tuple
                        parts = [p.strip() for p in match if p and p.strip()]
                        device_name = f"{brand.replace('_', ' ')} {' '.join(parts)}"
                    else:
                        device_name = f"{brand.replace('_', ' ')} {match}"

                    # Clean up device name
                    device_name = device_name.strip().title()
                    device_name = re.sub(r'\s+', ' ', device_name)  # Remove extra spaces

                    self.new_entities['devices'].add(device_name)
                    learned['device'] = device_name
                    learned['device_brand'] = brand.replace('_', ' ').split()[0].title()

                    # More specific brand identification for L2 subcategory
                    if 'iphone' in brand:
                        learned['device_subcategory'] = 'Apple iPhone'
                    elif 'samsung' in brand:
                        if 'galaxy_s' in brand:
                            learned['device_subcategory'] = 'Samsung Galaxy S Series'
                        elif 'galaxy_a' in brand:
                            learned['device_subcategory'] = 'Samsung Galaxy A Series'
                        elif 'galaxy_note' in brand:
                            learned['device_subcategory'] = 'Samsung Galaxy Note'
                        elif 'galaxy_z' in brand:
                            learned['device_subcategory'] = 'Samsung Foldables'
                        else:
                            learned['device_subcategory'] = 'Samsung Smartphones'
                    elif 'pixel' in brand:
                        learned['device_subcategory'] = 'Google Pixel'
                    elif 'oneplus' in brand:
                        learned['device_subcategory'] = 'OnePlus'
                    elif 'xiaomi' in brand:
                        learned['device_subcategory'] = 'Xiaomi/Redmi'
                    else:
                        learned['device_subcategory'] = f"{learned['device_brand']} Smartphones"

                    break  # Take first match
                break  # Stop after finding first brand match

        # Extract plan types
        plan_patterns = [
            (r'\b(\w+)\s+plan\b', 'plan'),
            (r'\b(\d+)\s*(?:gb|GB)\s+data\b', 'data_plan'),
            (r'\b(\w+)\s+(?:subscription|service)\b', 'service'),
        ]

        for pattern, plan_type in plan_patterns:
            matches = re.findall(pattern, query_lower)
            if matches:
                for match in matches:
                    if match not in ['prepaid', 'postpaid', 'unlimited', 'family']:  # Skip known
                        self.new_entities['plans'].add(match)
                        learned['plan_type'] = match

        # Extract internet/connectivity types
        internet_patterns = [
            r'\b(\w+)\s+(?:internet|broadband|wifi|5g|6g)\b',
            r'\b(fiber|cable|dsl|satellite)\s+',
        ]

        for pattern in internet_patterns:
            matches = re.findall(pattern, query_lower)
            if matches:
                for match in matches:
                    if match not in ['5g', 'fiber', 'cable']:  # Skip known
                        self.new_entities['services'].add(match)
                        learned['service_type'] = match

        # Detect comparison queries
        if ' vs ' in query_lower or ' versus ' in query_lower or 'compare' in query_lower:
            learned['intent'] = 'Comparative'
            learned['pattern_type'] = 'comparison'

        # Detect question queries
        if any(q in query_lower for q in ['how', 'what', 'why', 'when', 'where', 'which']):
            learned['intent'] = 'Informational'
            learned['pattern_type'] = 'question'

        # Detect purchase intent
        if any(w in query_lower for w in ['buy', 'purchase', 'order', 'get', 'price']):
            learned['intent'] = 'Transactional'
            learned['pattern_type'] = 'purchase'

        return learned

    def suggest_new_classification(self, query: str, learned_info: dict) -> dict:
        """Suggest a new classification based on learned patterns"""
        suggestion = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'confidence': 0
        }

        # Determine L1 category
        if learned_info.get('device'):
            # L1: Always "Devices" for device-related queries
            suggestion['L1_category'] = 'Devices'
            suggestion['confidence'] += 30

            # L2: Use specific device subcategory (e.g., "Apple iPhone", "Samsung Galaxy S Series")
            device_subcategory = learned_info.get('device_subcategory', 'Smartphones')
            suggestion['L2_subcategory'] = device_subcategory
            suggestion['confidence'] += 20

            # Get device name for L4 topic creation
            device = learned_info['device']

            # L3: Intent-based classification with L4 topic generation
            if learned_info.get('pattern_type') == 'comparison':
                # L3: Comparative Intent
                suggestion['L3_intent'] = 'Comparative'

                # L4: Specific comparison topic
                suggestion['L4_topic'] = f"{device} Comparison"
                suggestion['confidence'] += 40

            elif learned_info.get('pattern_type') == 'purchase':
                # L3: Transactional Intent
                suggestion['L3_intent'] = 'Transactional'

                # L4: Purchase-specific topic
                suggestion['L4_topic'] = f"{device} Purchase"
                suggestion['confidence'] += 40

            elif learned_info.get('pattern_type') == 'question':
                # L3: Informational Intent
                suggestion['L3_intent'] = 'Informational'

                # L4: Information/specs topic
                suggestion['L4_topic'] = f"{device} Specifications"
                suggestion['confidence'] += 30

            else:
                # Default: General informational
                suggestion['L3_intent'] = 'Informational'
                suggestion['L4_topic'] = f"{device} Information"
                suggestion['confidence'] += 20

        elif learned_info.get('plan_type'):
            suggestion['L1_category'] = 'Mobile Plans'
            suggestion['L2_subcategory'] = f"{learned_info['plan_type'].title()} Plans"
            suggestion['L4_topic'] = f"{learned_info['plan_type'].title()} Plan Information"
            suggestion['L3_intent'] = learned_info.get('intent', 'Informational')
            suggestion['confidence'] += 50

        elif learned_info.get('service_type'):
            suggestion['L1_category'] = 'Internet Services'
            suggestion['L2_subcategory'] = f"{learned_info['service_type'].title()} Internet"
            suggestion['L4_topic'] = f"{learned_info['service_type'].title()} Internet Information"
            suggestion['L3_intent'] = learned_info.get('intent', 'Informational')
            suggestion['confidence'] += 50

        return suggestion

    def update_decision_tree(self, suggestions: list, min_confidence: int = 50):
        """Update the decision tree with high-confidence suggestions"""

        # Load current tree
        with open(self.decision_tree_path, 'r') as f:
            tree = json.load(f)

        # Backup
        backup_path = self.decision_tree_path.replace('.json', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        with open(backup_path, 'w') as f:
            json.dump(tree, f, indent=2)

        # Filter high-confidence suggestions
        high_confidence = [s for s in suggestions if s.get('confidence', 0) >= min_confidence]

        # Group by L1/L2/L4
        grouped = defaultdict(lambda: defaultdict(list))
        for sugg in high_confidence:
            l1 = sugg.get('L1_category', 'Unknown')
            l2 = sugg.get('L2_subcategory', 'Unknown')
            l4 = sugg.get('L4_topic', 'Unknown')
            grouped[l1][l2].append(sugg)

        added_count = 0

        # Add to tree
        for l1_name, l2_dict in grouped.items():
            # Find or create L1 category
            l1_category = None
            for cat in tree['taxonomy']['L1_categories']:
                if cat['name'] == l1_name:
                    l1_category = cat
                    break

            if not l1_category:
                # Create new L1
                new_l1_id = f"L1_{len(tree['taxonomy']['L1_categories']) + 1:03d}"
                l1_category = {
                    'id': new_l1_id,
                    'name': l1_name,
                    'slug': l1_name.lower().replace(' ', '-'),
                    'priority': 'medium',
                    'monthly_search_volume': 10000,
                    'business_value': 'medium',
                    'L2_subcategories': []
                }
                tree['taxonomy']['L1_categories'].append(l1_category)

            for l2_name, suggestions_list in l2_dict.items():
                # Find or create L2 subcategory
                l2_subcategory = None
                for sub in l1_category.get('L2_subcategories', []):
                    if sub['name'] == l2_name:
                        l2_subcategory = sub
                        break

                if not l2_subcategory:
                    # Create new L2
                    total_l2 = sum(len(cat.get('L2_subcategories', [])) for cat in tree['taxonomy']['L1_categories'])
                    new_l2_id = f"L2_{total_l2 + 1:03d}"
                    l2_subcategory = {
                        'id': new_l2_id,
                        'name': l2_name,
                        'slug': l2_name.lower().replace(' ', '-'),
                        'parent': l1_category['id'],
                        'monthly_search_volume': 5000,
                        'L3_intents': []
                    }
                    l1_category.setdefault('L2_subcategories', []).append(l2_subcategory)

                # Group by intent
                intent_groups = defaultdict(list)
                for sugg in suggestions_list:
                    intent = sugg.get('L3_intent', 'Informational')
                    intent_groups[intent].append(sugg)

                for intent, intent_suggestions in intent_groups.items():
                    # Find or create L3 intent
                    l3_intent = None
                    for int_obj in l2_subcategory.get('L3_intents', []):
                        if int_obj['intent_category'] == intent:
                            l3_intent = int_obj
                            break

                    if not l3_intent:
                        # Create new L3
                        total_l3 = sum(len(sub.get('L3_intents', []))
                                     for cat in tree['taxonomy']['L1_categories']
                                     for sub in cat.get('L2_subcategories', []))
                        new_l3_id = f"L3_{total_l3 + 1:03d}"

                        # Determine intent details
                        intent_details = {
                            'Transactional': {
                                'subcategory': 'Direct Purchase Intent',
                                'commercial_score': 90,
                                'conversion_probability': '10-18%',
                                'funnel_stage': 'Purchase'
                            },
                            'Informational': {
                                'subcategory': 'Educational Intent',
                                'commercial_score': 30,
                                'conversion_probability': '2-4%',
                                'funnel_stage': 'Awareness'
                            },
                            'Comparative': {
                                'subcategory': 'Direct Comparison',
                                'commercial_score': 70,
                                'conversion_probability': '6-11%',
                                'funnel_stage': 'Consideration'
                            }
                        }

                        details = intent_details.get(intent, intent_details['Informational'])

                        l3_intent = {
                            'id': new_l3_id,
                            'intent_category': intent,
                            'intent_subcategory': details['subcategory'],
                            'commercial_score': details['commercial_score'],
                            'conversion_probability': details['conversion_probability'],
                            'conversion_window': '7-21 days',
                            'funnel_stage': details['funnel_stage'],
                            'L4_topics': []
                        }
                        l2_subcategory.setdefault('L3_intents', []).append(l3_intent)

                    # Add L4 topics and L5 keywords
                    for sugg in intent_suggestions:
                        l4_topic_name = sugg.get('L4_topic', 'Unknown Topic')

                        # Check if topic already exists
                        topic_exists = any(t['topic'] == l4_topic_name for t in l3_intent.get('L4_topics', []))

                        if not topic_exists:
                            total_l4 = sum(len(intent.get('L4_topics', []))
                                         for cat in tree['taxonomy']['L1_categories']
                                         for sub in cat.get('L2_subcategories', [])
                                         for intent in sub.get('L3_intents', []))
                            total_l5 = sum(len(topic.get('L5_keywords', []))
                                         for cat in tree['taxonomy']['L1_categories']
                                         for sub in cat.get('L2_subcategories', [])
                                         for intent in sub.get('L3_intents', [])
                                         for topic in intent.get('L4_topics', []))

                            new_l4_id = f"L4_{total_l4 + 1:03d}"
                            new_l5_id = f"L5_{total_l5 + 1:03d}"

                            new_l4_topic = {
                                'id': new_l4_id,
                                'topic': l4_topic_name,
                                'slug': l4_topic_name.lower().replace(' ', '-'),
                                'parent_intent': l3_intent['id'],
                                'content_type': 'educational_guide',
                                'url_structure': f"/learn/{l1_category['slug']}/{l4_topic_name.lower().replace(' ', '-')}/",
                                'primary_cta': 'Learn More',
                                'secondary_cta': 'Compare Options',
                                'L5_keywords': [
                                    {
                                        'id': new_l5_id,
                                        'keyword': sugg['query'].lower(),
                                        'search_volume': 100,
                                        'keyword_difficulty': 35,
                                        'cpc': 2.50,
                                        'intent_score': details['commercial_score'],
                                        'parent_topic': new_l4_id,
                                        'source': 'auto_learned',
                                        'learned_at': sugg['timestamp'],
                                        'confidence': sugg['confidence']
                                    }
                                ]
                            }

                            l3_intent.setdefault('L4_topics', []).append(new_l4_topic)
                            added_count += 1

        # Update metadata
        tree['classification_system']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        tree['classification_system']['version'] = f"{tree['classification_system']['version']}.{added_count}"

        # Save updated tree
        with open(self.decision_tree_path, 'w') as f:
            json.dump(tree, f, indent=2)

        return {
            'added_count': added_count,
            'backup_path': backup_path,
            'new_entities': {k: list(v) for k, v in self.new_entities.items()}
        }

    def get_learning_summary(self) -> dict:
        """Get summary of what has been learned"""
        return {
            'new_devices': list(self.new_entities['devices']),
            'new_plans': list(self.new_entities['plans']),
            'new_services': list(self.new_entities['services']),
            'total_patterns': sum(len(v) for v in self.new_entities.values())
        }


def test_learning():
    """Test the learning engine"""
    learning_engine = LearningEngine('/Users/venkatapagadala/Desktop/telecom-classification.json')

    test_queries = [
        "iphone 17 pro max vs iphone air",
        "samsung galaxy s25 ultra price",
        "pixel 9 pro xl review",
        "student plan unlimited data",
        "satellite internet rural areas",
        "6g network technology",
        "oneplus 12 pro buy",
        "compare iphone 16 and pixel 9",
    ]

    suggestions = []
    for query in test_queries:
        learned = learning_engine.analyze_unclassified(query)
        if learned:
            suggestion = learning_engine.suggest_new_classification(query, learned)
            suggestions.append(suggestion)
            print(f"\nQuery: {query}")
            print(f"Learned: {learned}")
            print(f"Suggestion: {suggestion}")

    print(f"\n\nLearning Summary:")
    print(json.dumps(learning_engine.get_learning_summary(), indent=2))

    return suggestions


if __name__ == '__main__':
    suggestions = test_learning()
