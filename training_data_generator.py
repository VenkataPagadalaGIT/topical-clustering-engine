#!/usr/bin/env python3
"""
Training Data Generator for Topical Clustering Engine
Uses DataForSEO API to pull comprehensive telecom keyword data
and auto-generate training entries for the classification system.
"""

import json
import requests
import os
import base64
from typing import Dict, List, Optional
from datetime import datetime
import time

class DataForSEOClient:
    """Client for DataForSEO API"""

    BASE_URL = "https://api.dataforseo.com/v3"

    def __init__(self, username: str, password: str):
        self.auth = base64.b64encode(f"{username}:{password}".encode()).decode()
        self.headers = {
            "Authorization": f"Basic {self.auth}",
            "Content-Type": "application/json"
        }

    def _request(self, endpoint: str, data: List[Dict]) -> Dict:
        """Make API request"""
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def get_keyword_suggestions(self, seed_keyword: str, location_code: int = 2840,
                                language_code: str = "en", limit: int = 100) -> List[Dict]:
        """Get keyword suggestions for a seed keyword"""
        data = [{
            "keyword": seed_keyword,
            "location_code": location_code,
            "language_code": language_code,
            "include_seed_keyword": True,
            "limit": limit
        }]
        result = self._request("keywords_data/google_ads/keywords_for_keywords/live", data)

        keywords = []
        if result.get("tasks"):
            for task in result["tasks"]:
                if task.get("result"):
                    for item in task["result"]:
                        keywords.append({
                            "keyword": item.get("keyword", ""),
                            "search_volume": item.get("search_volume", 0),
                            "cpc": item.get("cpc", 0),
                            "competition": item.get("competition", 0),
                            "competition_level": item.get("competition_level", "")
                        })
        return keywords

    def get_keyword_ideas(self, seed_keywords: List[str], location_code: int = 2840,
                          language_code: str = "en", limit: int = 500) -> List[Dict]:
        """Get keyword ideas from multiple seed keywords"""
        data = [{
            "keywords": seed_keywords,
            "location_code": location_code,
            "language_code": language_code,
            "limit": limit
        }]
        result = self._request("keywords_data/google_ads/keywords_for_keywords/live", data)

        keywords = []
        if result.get("tasks"):
            for task in result["tasks"]:
                if task.get("result"):
                    for item in task["result"]:
                        keywords.append({
                            "keyword": item.get("keyword", ""),
                            "search_volume": item.get("search_volume", 0),
                            "cpc": item.get("cpc", 0),
                            "competition": item.get("competition", 0)
                        })
        return keywords

    def get_serp_competitors(self, keyword: str, location_code: int = 2840) -> List[Dict]:
        """Get SERP results for a keyword"""
        data = [{
            "keyword": keyword,
            "location_code": location_code,
            "language_code": "en",
            "depth": 10
        }]
        result = self._request("serp/google/organic/live/regular", data)

        competitors = []
        if result.get("tasks"):
            for task in result["tasks"]:
                if task.get("result"):
                    for res in task["result"]:
                        for item in res.get("items", []):
                            if item.get("type") == "organic":
                                competitors.append({
                                    "domain": item.get("domain", ""),
                                    "url": item.get("url", ""),
                                    "title": item.get("title", ""),
                                    "rank": item.get("rank_group", 0)
                                })
        return competitors


class TelecomTrainingDataGenerator:
    """Generate comprehensive telecom training data"""

    # Comprehensive telecom seed keywords by category
    TELECOM_CATEGORIES = {
        "L1_001": {
            "name": "Mobile Plans",
            "subcategories": {
                "prepaid": [
                    "prepaid phone plans", "no contract plans", "pay as you go",
                    "prepaid unlimited", "prepaid family plans", "cheap prepaid",
                    "best prepaid carriers", "prepaid vs postpaid", "prepaid data plans"
                ],
                "postpaid": [
                    "monthly phone plans", "contract phone plans", "postpaid unlimited",
                    "best postpaid plans", "phone plan with device", "2 year contract plans"
                ],
                "unlimited": [
                    "unlimited data plan", "unlimited talk text", "truly unlimited",
                    "unlimited hotspot", "unlimited premium data", "best unlimited plans"
                ],
                "family": [
                    "family phone plan", "multi line plans", "family unlimited",
                    "best family plans", "4 line family plan", "family plan deals"
                ],
                "business": [
                    "business phone plan", "corporate mobile plan", "enterprise wireless",
                    "business unlimited", "small business phone plans", "fleet mobile plans"
                ],
                "senior": [
                    "senior phone plans", "55+ plans", "aarp phone plans",
                    "senior citizen mobile", "elderly phone plans", "simple phone plans seniors"
                ],
                "student": [
                    "student phone plans", "college student plans", "student discount wireless",
                    "cheap plans for students", "university phone deals"
                ],
                "international": [
                    "international calling plan", "international roaming", "global phone plan",
                    "international travel plan", "overseas calling", "international data roaming"
                ]
            }
        },
        "L1_002": {
            "name": "Devices",
            "subcategories": {
                "iphone": [
                    "iphone 15", "iphone 15 pro", "iphone 15 pro max", "iphone 15 plus",
                    "buy iphone", "iphone deals", "iphone trade in", "refurbished iphone",
                    "iphone financing", "iphone upgrade", "iphone comparison"
                ],
                "samsung": [
                    "samsung galaxy s24", "galaxy s24 ultra", "samsung galaxy z flip",
                    "samsung galaxy z fold", "samsung phone deals", "samsung trade in",
                    "galaxy a series", "samsung vs iphone", "best samsung phone"
                ],
                "google_pixel": [
                    "google pixel 8", "pixel 8 pro", "pixel phone deals",
                    "pixel vs iphone", "pixel trade in", "google pixel features"
                ],
                "budget_phones": [
                    "cheap smartphones", "budget android phones", "phones under 200",
                    "affordable smartphones", "best budget phones", "entry level phones"
                ],
                "accessories": [
                    "phone cases", "screen protectors", "wireless chargers",
                    "phone accessories", "earbuds", "smartwatch", "phone mount"
                ],
                "tablets": [
                    "ipad deals", "samsung tablet", "android tablet",
                    "tablet with cellular", "tablet data plan", "best tablets"
                ],
                "smartwatches": [
                    "apple watch", "samsung galaxy watch", "smartwatch deals",
                    "smartwatch with cellular", "fitness tracker", "best smartwatches"
                ]
            }
        },
        "L1_003": {
            "name": "Internet Services",
            "subcategories": {
                "home_internet": [
                    "home internet plans", "best home internet", "internet service providers",
                    "cheap home internet", "internet deals near me", "fastest home internet"
                ],
                "fiber": [
                    "fiber internet", "fiber optic plans", "gigabit internet",
                    "fiber availability", "fiber vs cable", "best fiber internet"
                ],
                "5g_home": [
                    "5g home internet", "5g wireless internet", "fixed wireless internet",
                    "5g home router", "5g internet speeds", "5g availability"
                ],
                "cable": [
                    "cable internet", "cable internet plans", "xfinity internet",
                    "spectrum internet", "cox internet", "cable vs fiber"
                ],
                "dsl": [
                    "dsl internet", "dsl plans", "dsl speed", "dsl availability",
                    "at&t dsl", "centurylink dsl"
                ],
                "rural": [
                    "rural internet", "internet for rural areas", "satellite internet",
                    "starlink", "hughesnet", "viasat", "rural broadband"
                ],
                "business_internet": [
                    "business internet", "enterprise internet", "dedicated internet",
                    "business fiber", "commercial internet", "office internet"
                ]
            }
        },
        "L1_004": {
            "name": "TV & Streaming",
            "subcategories": {
                "streaming": [
                    "streaming services", "best streaming", "streaming bundles",
                    "live tv streaming", "streaming deals", "cord cutting"
                ],
                "cable_tv": [
                    "cable tv plans", "cable packages", "cable tv deals",
                    "cable channels", "premium channels", "sports packages"
                ],
                "bundles": [
                    "internet tv bundle", "triple play bundle", "phone internet tv",
                    "best bundles", "bundle deals", "package discounts"
                ]
            }
        },
        "L1_005": {
            "name": "Coverage & Network",
            "subcategories": {
                "coverage": [
                    "coverage map", "cell coverage", "network coverage",
                    "coverage in my area", "best coverage", "rural coverage"
                ],
                "5g": [
                    "5g coverage", "5g network", "5g map", "5g speed",
                    "5g phones", "5g availability", "5g vs 4g"
                ],
                "signal": [
                    "cell signal booster", "improve signal", "signal strength",
                    "dead zones", "network extender", "wifi calling"
                ]
            }
        },
        "L1_006": {
            "name": "Customer Support",
            "subcategories": {
                "billing": [
                    "pay bill", "bill payment", "autopay", "billing issues",
                    "payment options", "bill due date", "paperless billing"
                ],
                "account": [
                    "my account", "login", "account management", "change plan",
                    "upgrade account", "add line", "remove line"
                ],
                "technical": [
                    "technical support", "troubleshooting", "phone not working",
                    "no service", "dropped calls", "slow data", "reset network"
                ],
                "activation": [
                    "activate phone", "activate sim", "port number",
                    "transfer number", "new activation", "esim activation"
                ]
            }
        },
        "L1_007": {
            "name": "Deals & Promotions",
            "subcategories": {
                "phone_deals": [
                    "phone deals", "free phone", "bogo phone", "trade in deals",
                    "phone discounts", "phone promotions", "best phone deals"
                ],
                "plan_deals": [
                    "plan deals", "discount plans", "promo codes",
                    "limited time offers", "seasonal deals", "black friday"
                ],
                "switching": [
                    "switch carriers", "switching deals", "port in offers",
                    "carrier switch bonus", "bring your phone", "byod deals"
                ]
            }
        }
    }

    # Intent patterns for classification
    INTENT_PATTERNS = {
        "transactional": {
            "keywords": ["buy", "purchase", "order", "get", "shop", "deal", "price", "cost", "cheap", "free"],
            "commercial_score": 90,
            "funnel_stage": "Purchase"
        },
        "commercial_investigation": {
            "keywords": ["best", "top", "review", "compare", "vs", "versus", "comparison", "rating"],
            "commercial_score": 70,
            "funnel_stage": "Consideration"
        },
        "informational": {
            "keywords": ["what is", "how to", "guide", "tutorial", "learn", "explain", "understand"],
            "commercial_score": 30,
            "funnel_stage": "Awareness"
        },
        "navigational": {
            "keywords": ["login", "my account", "customer service", "support", "contact", "near me", "store"],
            "commercial_score": 40,
            "funnel_stage": "Navigation"
        },
        "local": {
            "keywords": ["near me", "in my area", "local", "nearby", "closest", "location"],
            "commercial_score": 75,
            "funnel_stage": "Decision"
        }
    }

    def __init__(self, dataforseo_username: str, dataforseo_password: str):
        self.client = DataForSEOClient(dataforseo_username, dataforseo_password)
        self.generated_data = {
            "classification_system": {
                "version": "2.0",
                "industry": "telecommunications",
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
                "total_keywords": 0,
                "total_topics": 0,
                "description": "Comprehensive telecom classification with DataForSEO data"
            },
            "taxonomy": {
                "L1_categories": []
            }
        }

    def detect_intent(self, keyword: str) -> Dict:
        """Detect search intent from keyword"""
        keyword_lower = keyword.lower()

        for intent_type, config in self.INTENT_PATTERNS.items():
            for pattern in config["keywords"]:
                if pattern in keyword_lower:
                    return {
                        "intent_category": intent_type.replace("_", " ").title(),
                        "commercial_score": config["commercial_score"],
                        "funnel_stage": config["funnel_stage"]
                    }

        # Default to informational
        return {
            "intent_category": "Informational",
            "commercial_score": 40,
            "funnel_stage": "Awareness"
        }

    def generate_topic_from_keyword(self, keyword: str) -> str:
        """Generate a topic name from keyword"""
        # Remove common words and capitalize
        stop_words = ["the", "a", "an", "for", "to", "of", "in", "on", "with", "and", "or"]
        words = keyword.split()
        topic_words = [w.capitalize() for w in words if w.lower() not in stop_words]
        return " ".join(topic_words[:4])  # Max 4 words

    def pull_keywords_for_category(self, category_id: str, subcategory: str,
                                   seed_keywords: List[str], limit: int = 50) -> List[Dict]:
        """Pull keywords from DataForSEO for a subcategory"""
        print(f"  Pulling keywords for {subcategory}...")

        all_keywords = []
        for seed in seed_keywords[:3]:  # Use first 3 seeds to save API calls
            try:
                keywords = self.client.get_keyword_suggestions(seed, limit=limit)
                all_keywords.extend(keywords)
                time.sleep(0.5)  # Rate limiting
            except Exception as e:
                print(f"    Error pulling {seed}: {e}")

        # Deduplicate
        seen = set()
        unique_keywords = []
        for kw in all_keywords:
            if kw["keyword"] not in seen:
                seen.add(kw["keyword"])
                unique_keywords.append(kw)

        print(f"    Found {len(unique_keywords)} unique keywords")
        return unique_keywords

    def build_taxonomy(self, use_api: bool = True, keywords_per_subcategory: int = 30):
        """Build complete taxonomy with DataForSEO data"""
        print("Building telecom taxonomy...")

        keyword_id = 1
        topic_id = 1
        total_keywords = 0
        total_topics = 0

        for cat_id, category in self.TELECOM_CATEGORIES.items():
            print(f"\nProcessing {category['name']}...")

            l1_entry = {
                "id": cat_id,
                "name": category["name"],
                "slug": category["name"].lower().replace(" ", "-"),
                "L2_subcategories": []
            }

            for subcat_name, seed_keywords in category["subcategories"].items():
                subcat_id = f"L2_{str(len(l1_entry['L2_subcategories']) + 1).zfill(3)}"

                # Pull keywords from API or use seeds
                if use_api:
                    keywords = self.pull_keywords_for_category(cat_id, subcat_name, seed_keywords,
                                                               limit=keywords_per_subcategory)
                else:
                    keywords = [{"keyword": kw, "search_volume": 1000, "cpc": 2.0, "competition": 0.5}
                               for kw in seed_keywords]

                # Group keywords by intent
                intent_groups = {}
                for kw in keywords:
                    intent = self.detect_intent(kw["keyword"])
                    intent_key = intent["intent_category"]
                    if intent_key not in intent_groups:
                        intent_groups[intent_key] = {
                            "intent": intent,
                            "keywords": []
                        }
                    intent_groups[intent_key]["keywords"].append(kw)

                # Build L2 entry
                l2_entry = {
                    "id": subcat_id,
                    "name": subcat_name.replace("_", " ").title(),
                    "slug": subcat_name,
                    "L3_intents": []
                }

                for intent_name, intent_data in intent_groups.items():
                    l3_id = f"L3_{str(topic_id).zfill(3)}"

                    # Group keywords into topics (max 10 per topic)
                    topic_keywords = intent_data["keywords"]
                    topics = []

                    for i in range(0, len(topic_keywords), 10):
                        topic_batch = topic_keywords[i:i+10]
                        if topic_batch:
                            topic_name = self.generate_topic_from_keyword(topic_batch[0]["keyword"])
                            l4_id = f"L4_{str(topic_id).zfill(3)}"

                            l5_keywords = []
                            for kw in topic_batch:
                                l5_keywords.append({
                                    "id": f"L5_{str(keyword_id).zfill(5)}",
                                    "keyword": kw["keyword"],
                                    "search_volume": kw.get("search_volume", 0),
                                    "cpc": kw.get("cpc", 0),
                                    "competition": kw.get("competition", 0),
                                    "intent_score": intent_data["intent"]["commercial_score"]
                                })
                                keyword_id += 1
                                total_keywords += 1

                            topics.append({
                                "id": l4_id,
                                "topic": topic_name,
                                "slug": topic_name.lower().replace(" ", "-"),
                                "content_type": "landing_page" if intent_data["intent"]["commercial_score"] > 70 else "guide",
                                "L5_keywords": l5_keywords
                            })
                            topic_id += 1
                            total_topics += 1

                    if topics:
                        l3_entry = {
                            "id": l3_id,
                            "intent_category": intent_name,
                            "commercial_score": intent_data["intent"]["commercial_score"],
                            "funnel_stage": intent_data["intent"]["funnel_stage"],
                            "L4_topics": topics
                        }
                        l2_entry["L3_intents"].append(l3_entry)

                if l2_entry["L3_intents"]:
                    l1_entry["L2_subcategories"].append(l2_entry)

            self.generated_data["taxonomy"]["L1_categories"].append(l1_entry)

        self.generated_data["classification_system"]["total_keywords"] = total_keywords
        self.generated_data["classification_system"]["total_topics"] = total_topics

        print(f"\nGenerated {total_keywords} keywords across {total_topics} topics")
        return self.generated_data

    def save_to_file(self, filepath: str):
        """Save generated data to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.generated_data, f, indent=2, ensure_ascii=False)
        print(f"Saved to {filepath}")

    def merge_with_existing(self, existing_path: str, output_path: str):
        """Merge generated data with existing knowledge base"""
        with open(existing_path, 'r', encoding='utf-8') as f:
            existing = json.load(f)

        # Merge keywords from generated data into existing structure
        existing_keywords = set()
        for l1 in existing.get("taxonomy", {}).get("L1_categories", []):
            for l2 in l1.get("L2_subcategories", []):
                for l3 in l2.get("L3_intents", []):
                    for l4 in l3.get("L4_topics", []):
                        for l5 in l4.get("L5_keywords", []):
                            existing_keywords.add(l5.get("keyword", "").lower())

        # Add new keywords that don't exist
        new_keywords_added = 0
        for l1 in self.generated_data["taxonomy"]["L1_categories"]:
            for l2 in l1.get("L2_subcategories", []):
                for l3 in l2.get("L3_intents", []):
                    for l4 in l3.get("L4_topics", []):
                        for l5 in l4.get("L5_keywords", []):
                            if l5["keyword"].lower() not in existing_keywords:
                                new_keywords_added += 1

        # For now, create a combined file
        merged = {
            "classification_system": {
                **existing.get("classification_system", {}),
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
                "total_keywords": existing.get("classification_system", {}).get("total_keywords", 0) + new_keywords_added
            },
            "taxonomy": existing.get("taxonomy", {}),
            "new_data": self.generated_data["taxonomy"]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)

        print(f"Merged data saved to {output_path}")
        print(f"Added {new_keywords_added} new keywords")


def main():
    """Main function to generate training data"""
    import argparse

    parser = argparse.ArgumentParser(description="Generate telecom training data")
    parser.add_argument("--username", help="DataForSEO username",
                       default=os.getenv("DATAFORSEO_USERNAME"))
    parser.add_argument("--password", help="DataForSEO password",
                       default=os.getenv("DATAFORSEO_PASSWORD"))
    parser.add_argument("--output", help="Output file path",
                       default="telecom-training-data-new.json")
    parser.add_argument("--no-api", action="store_true",
                       help="Generate without API calls (uses seed keywords only)")
    parser.add_argument("--keywords-per-subcategory", type=int, default=30,
                       help="Number of keywords to pull per subcategory")
    parser.add_argument("--merge", help="Path to existing JSON to merge with")

    args = parser.parse_args()

    if not args.username or not args.password:
        print("DataForSEO credentials required. Set DATAFORSEO_USERNAME and DATAFORSEO_PASSWORD")
        print("Or use --no-api flag to generate with seed keywords only")
        if not args.no_api:
            return

    generator = TelecomTrainingDataGenerator(
        args.username or "",
        args.password or ""
    )

    generator.build_taxonomy(
        use_api=not args.no_api,
        keywords_per_subcategory=args.keywords_per_subcategory
    )

    if args.merge:
        generator.merge_with_existing(args.merge, args.output)
    else:
        generator.save_to_file(args.output)

    print("\nDone! You can now use this data to train your Topical Clustering Engine.")


if __name__ == "__main__":
    main()
