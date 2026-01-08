#!/usr/bin/env python3
"""
Telecom Query Classifier
Classifies search queries into a 5-level hierarchical taxonomy
Enhanced with priority-based matching and intent detection
"""

import json
import re
from typing import Dict, Optional, List, Tuple
import os


class TelecomClassifier:
    """Classifies telecom-related search queries using a decision tree"""

    # Category priority for disambiguation (higher = more specific)
    CATEGORY_PRIORITY = {
        # High-value specific categories
        'Customer Service': 95,
        'Unlocking': 90,
        'Activation': 90,
        'Trade In': 88,
        'Switching': 85,
        'BYOD': 85,
        'International': 82,
        'Connected Devices': 80,

        # Medium-specific categories
        'Comparisons': 75,
        'Reviews': 75,
        'Perks': 72,
        'Accessories': 70,
        'SIM': 70,
        'Billing': 68,
        'Retail': 65,
        'Local': 65,
        'Coverage': 62,
        'Pricing': 60,
        'Deals': 58,
        'Family Plans': 55,
        'Prepaid': 55,
        'Postpaid': 55,

        # Broad categories (lower priority)
        'Mobile Plans': 40,
        'Devices': 35,
        'Features': 30,
        'Support': 25,
        'FAQ': 20,
        'Carriers': 15,
    }

    # Intent keywords for better classification (order matters - more specific first)
    INTENT_INDICATORS = {
        'customer_service': ['customer service', 'service number', 'contact support', 'call support', 'live chat', 'help line', 'support number', 'customer support'],
        'store': ['store near', 'store location', 'closest store', 'nearest store'],
        'retail': ['verizon store', 'att store', 't-mobile store', 'phone store'],
        'unlock': ['unlock', 'unlocked', 'unlocking', 'carrier unlock'],
        'switch': ['switch from', 'switch to', 'leave', 'leaving', 'port to', 'change carrier'],
        'coverage': ['coverage map', 'signal strength', 'network coverage'],
        'compare': [' vs ', ' versus ', 'compare', 'comparison', 'difference between'],
        'price': ['price', 'cost', 'how much', 'pricing', 'under $', 'cheap'],
        'review': ['review', 'reviews', 'rating', 'worth it', 'pros and cons'],
        'trade_in': ['trade in', 'trade-in', 'tradein', 'trade in value'],
        'activate': ['activate', 'activation', 'setup', 'set up'],
        'international': ['international calling', 'international plan', 'international roaming', 'roaming', 'abroad', 'overseas', 'travel plan'],
        'sim': ['esim', 'e-sim', 'sim card', 'what is esim', 'what is sim'],
        'connected_device': ['tablet plan', 'tablet cellular', 'ipad plan', 'smartwatch plan', 'apple watch plan', 'galaxy watch plan', 'wearable plan'],
        # Note: 'local' intent is detected via _has_location() with city names only
        # 'near me' should NOT trigger local - it depends on context (coverage near me vs stores near me)
        'plan': ['budget plan', 'budget phone plan', 'cheap plan', 'affordable plan'],
    }

    # Brand keywords for branded query detection - EXPANDED
    CARRIER_BRANDS = [
        # Big 3
        'verizon', 'verizon wireless', 'vzw', 'at&t', 'att', 'at and t',
        't-mobile', 'tmobile', 't mobile', 'sprint',
        # Prepaid brands
        'metro', 'metro pcs', 'metropcs', 'cricket', 'cricket wireless',
        'boost', 'boost mobile', 'boost infinite', 'visible', 'visible+',
        'mint mobile', 'mint', 'us cellular', 'uscellular', 'us mobile',
        # MVNOs
        'google fi', 'fi by google', 'project fi', 'xfinity mobile', 'xfinity',
        'spectrum mobile', 'spectrum', 'straight talk', 'straighttalk',
        'total wireless', 'total by verizon', 'tracfone', 'simple mobile',
        'h2o wireless', 'h2o', 'republic wireless', 'ting', 'consumer cellular',
        'red pocket', 'ultra mobile', 'tello', 'twigby', 'wing mobile',
        'good2go', 'net10', 'page plus', 'lycamobile', 'gen mobile',
        'hello mobile', 'patriot mobile', 'freedompop', 'textnow',
        'credo mobile', 'airvoice', 'boom mobile', 'truconnect',
        # Regional
        'c spire', 'cspire', 'cellcom', 'gci', 'bluegrass cellular',
        # Business
        'verizon business', 'att business', 't-mobile business',
    ]

    PHONE_BRANDS = [
        # Apple
        'iphone', 'apple', 'ios',
        # Samsung
        'samsung', 'galaxy', 'galaxy s', 'galaxy z', 'galaxy a',
        # Google
        'pixel', 'google pixel', 'google',
        # Other major brands
        'motorola', 'moto', 'moto g', 'moto edge', 'razr',
        'oneplus', 'oneplus nord', 'oneplus open',
        'xiaomi', 'redmi', 'poco', 'mi phone',
        'nokia', 'lg', 'lg phone',
        'nothing', 'nothing phone',
        'tcl', 'zte', 'blu',
        'huawei', 'honor', 'oppo', 'vivo', 'realme',
        'asus', 'rog phone', 'sony', 'xperia',
        'blackberry', 'palm', 'cat phone', 'kyocera',
        # Connected devices
        'ipad', 'apple watch', 'airpods', 'galaxy tab', 'galaxy watch',
        'pixel watch', 'pixel buds', 'fitbit', 'garmin',
    ]

    # Location keywords for Local category detection
    LOCATION_KEYWORDS = [
        'los angeles', 'new york', 'chicago', 'houston', 'phoenix', 'philadelphia',
        'san antonio', 'san diego', 'dallas', 'san jose', 'austin', 'jacksonville',
        'fort worth', 'columbus', 'charlotte', 'seattle', 'denver', 'washington dc',
        'boston', 'nashville', 'detroit', 'portland', 'las vegas', 'memphis',
        'baltimore', 'milwaukee', 'albuquerque', 'tucson', 'fresno', 'sacramento',
        'kansas city', 'atlanta', 'miami', 'oakland', 'minneapolis', 'tulsa',
        'cleveland', 'new orleans', 'arlington', 'bakersfield', 'tampa', 'aurora',
        'honolulu', 'anaheim', 'santa ana', 'riverside', 'corpus christi', 'lexington',
        'st. louis', 'pittsburgh', 'stockton', 'cincinnati', 'anchorage', 'henderson',
    ]

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

    def _detect_intent(self, query: str) -> Optional[str]:
        """Detect the primary intent from query"""
        query_lower = query.lower()

        # Check for location-based queries (city name required for local intent)
        # "near me" alone should NOT trigger local - it could be coverage, stores, etc.
        if self._has_location(query_lower):
            return 'local'

        # Check for "vs" comparison pattern (very specific)
        if ' vs ' in query_lower or query_lower.endswith(' vs') or query_lower.startswith('vs '):
            return 'compare'

        # Check for customer service patterns (very specific - should always go to Customer Service)
        if 'customer service' in query_lower or 'service number' in query_lower or 'customer support' in query_lower:
            return 'customer_service'

        # Check for connected device patterns
        if any(x in query_lower for x in ['tablet plan', 'tablet cellular', 'tablet data']):
            return 'connected_device'

        # Check for international patterns
        if 'international' in query_lower and ('calling' in query_lower or 'plan' in query_lower):
            return 'international'

        # Check for plan-focused queries (budget/cheap plan)
        if 'budget' in query_lower and 'plan' in query_lower:
            return 'plan'

        for intent, indicators in self.INTENT_INDICATORS.items():
            for indicator in indicators:
                if indicator in query_lower:
                    return intent
        return None

    def _has_location(self, query: str) -> bool:
        """Check if query contains a city/location name"""
        for city in self.LOCATION_KEYWORDS:
            if city in query:
                return True
        return False

    def _detect_brand(self, query: str) -> Dict:
        """Detect if query is branded and identify the brand(s)"""
        query_lower = query.lower()
        result = {
            'is_branded': False,
            'brand_type': None,  # 'carrier', 'phone', or 'both'
            'carriers': [],
            'phone_brands': []
        }

        # Check for carrier brands
        for carrier in self.CARRIER_BRANDS:
            if carrier in query_lower:
                result['carriers'].append(carrier)
                result['is_branded'] = True

        # Check for phone brands
        for phone in self.PHONE_BRANDS:
            if phone in query_lower:
                result['phone_brands'].append(phone)
                result['is_branded'] = True

        # Determine brand type
        if result['carriers'] and result['phone_brands']:
            result['brand_type'] = 'both'
        elif result['carriers']:
            result['brand_type'] = 'carrier'
        elif result['phone_brands']:
            result['brand_type'] = 'phone'

        return result

    def _get_category_priority(self, category: str) -> int:
        """Get priority score for a category"""
        return self.CATEGORY_PRIORITY.get(category, 50)

    def _get_expected_category_from_intent(self, intent: Optional[str]) -> Optional[str]:
        """Map detected intent to expected category"""
        if not intent:
            return None
        intent_to_category = {
            'customer_service': 'Customer Service',
            'store': 'Retail',
            'retail': 'Retail',
            'unlock': 'Unlocking',
            'switch': 'Switching',
            'coverage': 'Coverage',
            'compare': 'Comparisons',
            'review': 'Reviews',
            'trade_in': 'Trade In',
            'activate': 'Activation',
            'international': 'International',
            'sim': 'SIM',
            'connected_device': 'Connected Devices',
            'local': 'Local',
            'plan': 'Mobile Plans',
        }
        return intent_to_category.get(intent)

    def _find_intent_aligned_match(self, query: str, query_words: set, target_category: str) -> Optional[Dict]:
        """Find a keyword match that aligns with the detected intent category"""
        best_match = None
        best_score = 0

        for keyword, classification in self.keywords_index.items():
            if classification['L1']['name'] == target_category:
                score = self._calculate_match_score(query, query_words, keyword)
                if score > best_score and score >= 0.5:
                    best_score = score
                    best_match = classification

        return best_match

    def _find_best_fuzzy_in_category(self, query: str, query_words: set, target_category: str) -> Optional[Dict]:
        """Find the best fuzzy match in a specific category, with lower threshold"""
        best_match = None
        best_score = 0

        for keyword, classification in self.keywords_index.items():
            if classification['L1']['name'] == target_category:
                score = self._calculate_match_score(query, query_words, keyword)
                # Lower threshold for strong intent matches
                if score > best_score and score >= 0.25:
                    best_score = score
                    best_match = classification

        return best_match

    def classify_text(self, query: str) -> Optional[Dict]:
        """
        Classify a search query into the taxonomy
        Returns classification with confidence score
        Uses multi-stage matching with intent detection and priority scoring
        """
        if not query or not query.strip():
            return None

        query_lower = query.lower().strip()
        query_words = set(query_lower.split())

        # Stage 1: Detect primary intent FIRST (for smart disambiguation)
        detected_intent = self._detect_intent(query_lower)

        # Stage 2: Exact match - but consider intent for disambiguation
        if query_lower in self.keywords_index:
            match = self.keywords_index[query_lower]
            actual_category = match['L1']['name']

            # Check if intent suggests a different category should be prioritized
            expected_category = self._get_expected_category_from_intent(detected_intent)
            if expected_category and actual_category != expected_category:
                # For strong intent signals, find the best match in the expected category
                alt_match = self._find_intent_aligned_match(query_lower, query_words, expected_category)
                if alt_match:
                    return self._format_result(alt_match, query, confidence=0.95)
                # Even if no exact match, if intent is strong, search harder
                if detected_intent in ['local', 'compare', 'customer_service', 'international', 'connected_device']:
                    best_fuzzy = self._find_best_fuzzy_in_category(query_lower, query_words, expected_category)
                    if best_fuzzy:
                        return self._format_result(best_fuzzy, query, confidence=0.85)

            return self._format_result(match, query, confidence=1.0)

        # Stage 3: Find all matching keywords with scores
        candidates = []

        # For very strong intent signals, restrict search to that category only
        restrict_to_category = None
        if detected_intent in ['customer_service']:
            restrict_to_category = self._get_expected_category_from_intent(detected_intent)

        for keyword, classification in self.keywords_index.items():
            category = classification['L1']['name']

            # If restricted, skip other categories
            if restrict_to_category and category != restrict_to_category:
                continue

            score = self._calculate_match_score(query_lower, query_words, keyword)
            if score >= 0.3:
                priority = self._get_category_priority(category)

                # Boost priority if intent matches category
                if detected_intent:
                    if detected_intent == 'customer_service' and category == 'Customer Service':
                        priority += 60
                    elif detected_intent == 'store' and category == 'Retail':
                        priority += 50
                    elif detected_intent == 'retail' and category == 'Retail':
                        priority += 40
                    elif detected_intent == 'unlock' and category == 'Unlocking':
                        priority += 50
                    elif detected_intent == 'switch' and category == 'Switching':
                        priority += 50
                    elif detected_intent == 'coverage' and category == 'Coverage':
                        priority += 40
                    elif detected_intent == 'compare' and category == 'Comparisons':
                        priority += 60
                    elif detected_intent == 'review' and category == 'Reviews':
                        priority += 40
                    elif detected_intent == 'trade_in' and category == 'Trade In':
                        priority += 50
                    elif detected_intent == 'activate' and category == 'Activation':
                        priority += 50
                    elif detected_intent == 'international' and category == 'International':
                        priority += 60
                    elif detected_intent == 'sim' and category == 'SIM':
                        priority += 60
                    elif detected_intent == 'connected_device' and category == 'Connected Devices':
                        priority += 60
                    elif detected_intent == 'local' and category == 'Local':
                        priority += 70
                    elif detected_intent == 'plan' and category == 'Mobile Plans':
                        priority += 30

                candidates.append({
                    'classification': classification,
                    'score': score,
                    'priority': priority,
                    'keyword': keyword
                })

        if candidates:
            # Sort by: 1) score (descending), 2) priority (descending), 3) keyword length (descending)
            candidates.sort(key=lambda x: (x['score'], x['priority'], len(x['keyword'])), reverse=True)

            # If top candidates have same score, prefer higher priority category
            top_score = candidates[0]['score']
            top_candidates = [c for c in candidates if c['score'] >= top_score - 0.05]

            if len(top_candidates) > 1:
                # Re-sort by priority
                top_candidates.sort(key=lambda x: x['priority'], reverse=True)

            best = top_candidates[0]
            return self._format_result(best['classification'], query, confidence=best['score'])

        # Stage 4: Pattern-based classification as fallback
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
        """Build a classification result from detected patterns with brand detection"""
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

        # Detect brand information for pattern-based results too
        brand_info = self._detect_brand(query)

        return {
            'query': query,
            'classification': {
                'L1': {'id': l1_id, 'name': l1_name},
                'L2': {
                    'id': 'L2_pattern',
                    'name': detected['plan_type'] or detected['device'] or 'General',
                    'is_branded': brand_info['is_branded'],
                    'brand_type': brand_info['brand_type'],
                    'detected_carriers': brand_info['carriers'],
                    'detected_phone_brands': brand_info['phone_brands']
                },
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
        """Format the classification result with brand detection"""
        # Detect brand information
        brand_info = self._detect_brand(query)

        return {
            'query': query,
            'classification': {
                'L1': match['L1'],
                'L2': {
                    **match['L2'],
                    'is_branded': brand_info['is_branded'],
                    'brand_type': brand_info['brand_type'],
                    'detected_carriers': brand_info['carriers'],
                    'detected_phone_brands': brand_info['phone_brands']
                },
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

    # Find the decision tree - prefer the 100K dataset
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Try 100K dataset first
    decision_tree_path = os.path.join(script_dir, 'telecom-classification-100K.json')

    if not os.path.exists(decision_tree_path):
        decision_tree_path = os.path.join(script_dir, 'telecom-classification-EXPANDED.json')

    if not os.path.exists(decision_tree_path):
        decision_tree_path = os.path.join(script_dir, 'telecom_app', 'telecom-classification-EXPANDED.json')

    print(f"Loading classifier from: {decision_tree_path}")
    classifier = TelecomClassifier(decision_tree_path)
    print(f"Loaded {len(classifier.keywords_index)} keywords into index")

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
