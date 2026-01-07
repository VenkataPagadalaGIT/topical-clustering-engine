#!/usr/bin/env python3
"""
Telecom Query Classifier
Classifies search queries into a 5-level hierarchical taxonomy
"""

import json
import re
from typing import Dict, Optional, List
import os


class TelecomClassifier:
    """Classifies telecom-related search queries using a decision tree"""

    def __init__(self, decision_tree_path: str):
        self.decision_tree_path = decision_tree_path
        self.taxonomy = None
        self.keywords_index = {}
        self.patterns = {}
        self._load_decision_tree()
        self._build_indexes()

    def _load_decision_tree(self):
        """Load the classification decision tree from JSON"""
        if not os.path.exists(self.decision_tree_path):
            # Try alternate path
            alt_path = os.path.join(os.path.dirname(self.decision_tree_path),
                                   'telecom_app', 'telecom-classification-EXPANDED.json')
            if os.path.exists(alt_path):
                self.decision_tree_path = alt_path
            else:
                raise FileNotFoundError(f"Decision tree not found: {self.decision_tree_path}")

        with open(self.decision_tree_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.taxonomy = data.get('taxonomy', data)
            self.metadata = data.get('classification_system', {})

    def _build_indexes(self):
        """Build keyword and pattern indexes for fast lookup"""
        if not self.taxonomy:
            return

        # Index all L5 keywords for exact/fuzzy matching
        l1_categories = self.taxonomy.get('L1_categories', [])

        for l1 in l1_categories:
            l1_info = {'id': l1['id'], 'name': l1['name'], 'slug': l1.get('slug', '')}

            for l2 in l1.get('L2_subcategories', []):
                l2_info = {'id': l2['id'], 'name': l2['name'], 'slug': l2.get('slug', '')}

                for l3 in l2.get('L3_intents', []):
                    l3_info = {
                        'id': l3['id'],
                        'intent_category': l3.get('intent_category', ''),
                        'intent_subcategory': l3.get('intent_subcategory', ''),
                        'commercial_score': l3.get('commercial_score', 0),
                        'funnel_stage': l3.get('funnel_stage', ''),
                        'conversion_probability': l3.get('conversion_probability', '')
                    }

                    for l4 in l3.get('L4_topics', []):
                        l4_info = {
                            'id': l4['id'],
                            'topic': l4.get('topic', ''),
                            'slug': l4.get('slug', ''),
                            'content_type': l4.get('content_type', ''),
                            'url_structure': l4.get('url_structure', ''),
                            'primary_cta': l4.get('primary_cta', ''),
                            'secondary_cta': l4.get('secondary_cta', '')
                        }

                        for l5 in l4.get('L5_keywords', []):
                            keyword = l5.get('keyword', '').lower().strip()
                            if keyword:
                                self.keywords_index[keyword] = {
                                    'L1': l1_info,
                                    'L2': l2_info,
                                    'L3': l3_info,
                                    'L4': l4_info,
                                    'L5': l5
                                }

        # Build common patterns for fuzzy matching
        self._build_patterns()

    def _build_patterns(self):
        """Build regex patterns for common query types"""
        self.patterns = {
            # Device patterns
            'iphone': r'\biphone\s*(\d+)?\s*(pro|max|plus|mini|se)?',
            'samsung': r'\b(samsung|galaxy)\s*(s|a|note|z|fold|flip)?\s*(\d+)?',
            'pixel': r'\bpixel\s*(\d+)?\s*(pro|a|xl)?',

            # Plan patterns
            'prepaid': r'\b(prepaid|pay\s*as\s*you\s*go|no\s*contract)',
            'postpaid': r'\b(postpaid|contract|monthly\s*plan)',
            'unlimited': r'\bunlimited\s*(data|talk|text|plan)?',
            'family': r'\b(family|shared|multi.?line)\s*plan',

            # Intent patterns
            'buy': r'\b(buy|purchase|get|order|shop)',
            'compare': r'\b(compare|vs|versus|difference|better)',
            'price': r'\b(price|cost|how\s*much|cheap|affordable|deal)',
            'review': r'\b(review|rating|worth|good|best)',
            'support': r'\b(help|support|issue|problem|fix|troubleshoot)',
            'upgrade': r'\b(upgrade|trade.?in|switch|change)',

            # Service patterns
            '5g': r'\b5g\b',
            'internet': r'\b(internet|wifi|wi-fi|broadband|fiber)',
            'streaming': r'\b(stream|netflix|hulu|disney|hbo)',
            'international': r'\b(international|roaming|abroad|travel)',
        }

    def classify_text(self, query: str) -> Optional[Dict]:
        """
        Classify a search query into the taxonomy
        Returns classification with confidence score
        """
        if not query or not query.strip():
            return None

        query_lower = query.lower().strip()
        query_words = set(query_lower.split())

        # Try exact match first
        if query_lower in self.keywords_index:
            match = self.keywords_index[query_lower]
            return self._format_result(match, query, confidence=1.0)

        # Try partial/fuzzy matching
        best_match = None
        best_score = 0

        for keyword, classification in self.keywords_index.items():
            score = self._calculate_match_score(query_lower, query_words, keyword)
            if score > best_score and score >= 0.3:
                best_score = score
                best_match = classification

        if best_match:
            return self._format_result(best_match, query, confidence=best_score)

        # Try pattern-based classification
        pattern_match = self._classify_by_patterns(query_lower)
        if pattern_match:
            return pattern_match

        return None

    def _calculate_match_score(self, query: str, query_words: set, keyword: str) -> float:
        """Calculate similarity score between query and keyword"""
        keyword_words = set(keyword.split())

        # Check if keyword is substring of query or vice versa
        if keyword in query:
            return 0.9
        if query in keyword:
            return 0.7

        # Word overlap score
        if keyword_words and query_words:
            overlap = len(keyword_words & query_words)
            union = len(keyword_words | query_words)
            jaccard = overlap / union if union > 0 else 0

            # Boost if all keyword words are in query
            if keyword_words <= query_words:
                return min(0.95, jaccard + 0.4)

            return jaccard

        return 0

    def _classify_by_patterns(self, query: str) -> Optional[Dict]:
        """Classify using regex patterns when exact match fails"""
        detected = {
            'device': None,
            'plan_type': None,
            'intent': None,
            'service': None
        }

        # Detect device
        for device in ['iphone', 'samsung', 'pixel']:
            if re.search(self.patterns[device], query, re.IGNORECASE):
                detected['device'] = device
                break

        # Detect plan type
        for plan in ['prepaid', 'postpaid', 'unlimited', 'family']:
            if re.search(self.patterns[plan], query, re.IGNORECASE):
                detected['plan_type'] = plan
                break

        # Detect intent
        for intent in ['buy', 'compare', 'price', 'review', 'support', 'upgrade']:
            if re.search(self.patterns[intent], query, re.IGNORECASE):
                detected['intent'] = intent
                break

        # Detect service
        for service in ['5g', 'internet', 'streaming', 'international']:
            if re.search(self.patterns[service], query, re.IGNORECASE):
                detected['service'] = service
                break

        # Build classification from detected patterns
        if any(detected.values()):
            return self._build_pattern_classification(query, detected)

        return None

    def _build_pattern_classification(self, query: str, detected: Dict) -> Dict:
        """Build a classification result from detected patterns"""
        # Determine L1 category
        if detected['device']:
            l1_name = "Devices"
            l1_id = "L1_002"
        elif detected['plan_type']:
            l1_name = "Mobile Plans"
            l1_id = "L1_001"
        elif detected['service'] == 'internet':
            l1_name = "Internet Services"
            l1_id = "L1_003"
        else:
            l1_name = "Mobile Plans"
            l1_id = "L1_001"

        # Determine intent
        intent_map = {
            'buy': ('Transactional', 'Direct Purchase Intent', 95, 'Purchase'),
            'compare': ('Commercial Investigation', 'Comparison Shopping', 75, 'Consideration'),
            'price': ('Commercial Investigation', 'Price Research', 80, 'Consideration'),
            'review': ('Informational', 'Product Research', 60, 'Awareness'),
            'support': ('Navigational', 'Customer Support', 30, 'Retention'),
            'upgrade': ('Transactional', 'Upgrade Intent', 85, 'Purchase'),
        }

        intent_info = intent_map.get(detected['intent'],
                                     ('Informational', 'General Research', 50, 'Awareness'))

        # Build topic from detected elements
        topic_parts = []
        if detected['device']:
            topic_parts.append(detected['device'].title())
        if detected['plan_type']:
            topic_parts.append(detected['plan_type'].title())
        if detected['service']:
            topic_parts.append(detected['service'].upper() if detected['service'] == '5g' else detected['service'].title())
        if detected['intent']:
            topic_parts.append(detected['intent'].title())

        topic = ' '.join(topic_parts) if topic_parts else 'General Query'

        return {
            'query': query,
            'classification': {
                'L1': {'id': l1_id, 'name': l1_name},
                'L2': {'id': 'L2_pattern', 'name': detected['plan_type'] or detected['device'] or 'General'},
                'L3': {
                    'intent_category': intent_info[0],
                    'intent_subcategory': intent_info[1],
                    'commercial_score': intent_info[2],
                    'funnel_stage': intent_info[3]
                },
                'L4': {'topic': topic, 'slug': topic.lower().replace(' ', '-')}
            },
            'confidence_score': 0.6,
            'match_type': 'pattern'
        }

    def _format_result(self, match: Dict, query: str, confidence: float) -> Dict:
        """Format the classification result"""
        return {
            'query': query,
            'classification': {
                'L1': match['L1'],
                'L2': match['L2'],
                'L3': {
                    'intent_category': match['L3'].get('intent_category', ''),
                    'intent_subcategory': match['L3'].get('intent_subcategory', ''),
                    'commercial_score': match['L3'].get('commercial_score', 0),
                    'funnel_stage': match['L3'].get('funnel_stage', ''),
                    'conversion_probability': match['L3'].get('conversion_probability', '')
                },
                'L4': match['L4'],
                'L5': match.get('L5', {})
            },
            'confidence_score': confidence,
            'match_type': 'exact' if confidence >= 0.95 else 'fuzzy'
        }

    def get_all_categories(self) -> List[Dict]:
        """Get all L1 categories"""
        if not self.taxonomy:
            return []
        return self.taxonomy.get('L1_categories', [])

    def get_category_topics(self, l1_id: str) -> List[Dict]:
        """Get all topics under a specific L1 category"""
        topics = []
        for l1 in self.taxonomy.get('L1_categories', []):
            if l1['id'] == l1_id:
                for l2 in l1.get('L2_subcategories', []):
                    for l3 in l2.get('L3_intents', []):
                        for l4 in l3.get('L4_topics', []):
                            topics.append({
                                'L2': l2['name'],
                                'L3': l3.get('intent_category', ''),
                                'L4': l4
                            })
        return topics


if __name__ == '__main__':
    # Test the classifier
    import sys

    # Find the decision tree
    script_dir = os.path.dirname(os.path.abspath(__file__))
    decision_tree_path = os.path.join(script_dir, 'telecom_app', 'telecom-classification-EXPANDED.json')

    if not os.path.exists(decision_tree_path):
        decision_tree_path = os.path.join(script_dir, 'telecom-classification-EXPANDED.json')

    print(f"Loading classifier from: {decision_tree_path}")
    classifier = TelecomClassifier(decision_tree_path)

    # Test queries
    test_queries = [
        "buy prepaid plan",
        "iphone 15 pro max",
        "compare unlimited plans",
        "5g coverage in my area",
        "samsung galaxy s24 price",
        "family plan deals"
    ]

    print("\nTest Classifications:")
    print("=" * 60)

    for query in test_queries:
        result = classifier.classify_text(query)
        if result:
            print(f"\nQuery: {query}")
            print(f"  L1: {result['classification']['L1']['name']}")
            print(f"  L4 Topic: {result['classification']['L4'].get('topic', 'N/A')}")
            print(f"  Intent: {result['classification']['L3']['intent_category']}")
            print(f"  Confidence: {result['confidence_score']:.2f}")
        else:
            print(f"\nQuery: {query} -> No classification")
