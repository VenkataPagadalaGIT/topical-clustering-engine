#!/usr/bin/env python3
"""
Generate 100,000+ telecom keywords for training data
Uses expanded seed keywords + variations + DataForSEO API with rate limiting
"""

import json
import itertools
import re
from typing import List, Dict
from datetime import datetime

class TelecomKeywordExpander:
    """Generate comprehensive telecom keyword variations"""

    # Carriers - Massively Expanded
    CARRIERS = [
        # Major carriers (all variations)
        "verizon", "verizon wireless", "vzw", "at&t", "att", "at and t", "at&t wireless",
        "t-mobile", "tmobile", "t mobile", "sprint", "sprint mobile",
        # Prepaid brands (all variations)
        "metro", "metro by t-mobile", "metro pcs", "metropcs", "cricket", "cricket wireless",
        "boost", "boost mobile", "boost infinite", "visible", "visible+", "visible plus",
        "mint mobile", "mint", "mint wireless", "us cellular", "uscellular", "us mobile", "usmobile",
        # MVNOs (expanded)
        "google fi", "fi by google", "project fi", "xfinity mobile", "xfinity wireless",
        "spectrum mobile", "spectrum wireless", "straight talk", "straighttalk", "straight talk wireless",
        "total wireless", "total by verizon", "tracfone", "tracfone wireless", "simple mobile",
        "h2o wireless", "h2o", "republic wireless", "ting", "ting mobile", "consumer cellular",
        "red pocket", "red pocket mobile", "ultra mobile", "ultramobile", "pure talk", "puretalk",
        "tello", "tello mobile", "twigby", "wing", "wing mobile", "good2go", "good2go mobile",
        "net10", "net10 wireless", "page plus", "page plus cellular", "lycamobile", "lyca mobile",
        "gen mobile", "black wireless", "reach mobile", "reach", "hello mobile", "hello",
        "patriot mobile", "patriot", "ting", "freedompop", "textnow", "textnow wireless",
        "puppy wireless", "credo mobile", "porting", "airvoice", "airvoice wireless",
        "boom mobile", "boom", "chit chat mobile", "easygo wireless", "go smart mobile",
        "jolt mobile", "mobi pos", "pix wireless", "rok mobile", "selectel wireless",
        "speedtalk mobile", "telcel america", "tempo", "truconnect", "truphone",
        "unreal mobile", "us mobile", "zip sim", "airvoice", "avo wireless",
        # Business/Enterprise
        "verizon business", "att business", "at&t business", "t-mobile business",
        "t-mobile for business", "verizon enterprise", "att enterprise",
        "sprint business", "corporate wireless", "business mobile",
        # Regional carriers
        "c spire", "cspire", "u.s. cellular", "us cellular", "cellcom", "nex-tech",
        "gci", "gci wireless", "bluegrass cellular", "carolina west wireless",
        "cellularone", "chat mobility", "chariton valley", "commnet wireless",
        "cross telephone", "east kentucky network", "farmers", "golden state cellular",
        "grundy", "i wireless", "illinois valley cellular", "inland cellular",
        "iwireless", "james valley", "mid-rivers", "mobiletel", "nex-tech wireless",
        "nortex", "northwest missouri cellular", "panhandle wireless", "peoples wireless",
        "pine cellular", "pioneer cellular", "plateau wireless", "rural cellular",
        "si wireless", "silver star", "smo", "sprocket", "strata networks",
        "syringa wireless", "thumb cellular", "triangle", "united wireless",
        "viaero", "vtelwireless", "west central wireless", "westlink"
    ]

    # Phone brands and models - Massively Expanded
    PHONES = {
        "iphone": [
            # Current generation
            "iphone", "iphone 16", "iphone 16 pro", "iphone 16 pro max", "iphone 16 plus", "iphone 16e",
            "iphone 15", "iphone 15 pro", "iphone 15 pro max", "iphone 15 plus",
            "iphone 14", "iphone 14 pro", "iphone 14 pro max", "iphone 14 plus",
            "iphone 13", "iphone 13 pro", "iphone 13 pro max", "iphone 13 mini",
            "iphone 12", "iphone 12 pro", "iphone 12 pro max", "iphone 12 mini",
            "iphone 11", "iphone 11 pro", "iphone 11 pro max",
            "iphone se", "iphone se 2024", "iphone se 3", "iphone se 4",
            "iphone xr", "iphone xs", "iphone xs max", "iphone x",
            # Variations
            "apple phone", "new iphone", "latest iphone", "newest iphone", "2024 iphone", "2025 iphone",
            "refurbished iphone", "used iphone", "certified pre owned iphone", "unlocked iphone",
            "cheap iphone", "iphone deals", "iphone trade in", "iphone upgrade",
            # Storage variants
            "iphone 128gb", "iphone 256gb", "iphone 512gb", "iphone 1tb",
            # Colors
            "iphone pro titanium", "iphone blue", "iphone pink", "iphone black", "iphone white"
        ],
        "samsung": [
            # Flagship S series
            "samsung", "galaxy", "samsung galaxy", "galaxy s24", "galaxy s24 ultra", "galaxy s24 plus", "galaxy s24 fe",
            "galaxy s23", "galaxy s23 ultra", "galaxy s23 plus", "galaxy s23 fe",
            "galaxy s22", "galaxy s22 ultra", "galaxy s22 plus", "galaxy s21", "galaxy s21 ultra",
            # Foldables
            "galaxy z flip", "galaxy z flip 6", "galaxy z flip 5", "galaxy z flip 4", "z flip",
            "galaxy z fold", "galaxy z fold 6", "galaxy z fold 5", "galaxy z fold 4", "z fold",
            "samsung flip", "samsung fold", "samsung foldable",
            # A series (budget/mid-range)
            "galaxy a54", "galaxy a55", "galaxy a34", "galaxy a35", "galaxy a24", "galaxy a25",
            "galaxy a14", "galaxy a15", "galaxy a04", "galaxy a05", "galaxy a series",
            # Other lines
            "galaxy xcover", "galaxy xcover 6 pro", "galaxy tab", "samsung tablet",
            # Variations
            "samsung phone", "new samsung", "latest samsung", "samsung deals", "samsung trade in",
            "refurbished samsung", "used samsung", "unlocked samsung", "certified samsung",
            # Storage
            "samsung 256gb", "samsung 512gb", "samsung 1tb"
        ],
        "google": [
            "pixel", "google pixel", "pixel 9", "pixel 9 pro", "pixel 9 pro xl", "pixel 9 pro fold",
            "pixel 8", "pixel 8 pro", "pixel 8a", "pixel 7", "pixel 7 pro", "pixel 7a",
            "pixel 6", "pixel 6 pro", "pixel 6a", "pixel 5", "pixel 5a",
            "pixel fold", "pixel watch", "pixel watch 2", "pixel buds",
            "google phone", "pixel deals", "pixel trade in", "unlocked pixel",
            "refurbished pixel", "used pixel", "new pixel", "latest pixel"
        ],
        "motorola": [
            "motorola", "moto", "moto g", "moto g power", "moto g power 2024", "moto g stylus",
            "moto g stylus 2024", "moto g play", "moto g 5g", "moto g pure",
            "motorola edge", "motorola edge plus", "motorola edge 2024", "moto edge",
            "motorola razr", "motorola razr plus", "razr plus", "razr 2024", "moto razr",
            "motorola thinkphone", "moto phone", "motorola deals", "motorola trade in"
        ],
        "oneplus": [
            "oneplus", "oneplus 12", "oneplus 12r", "oneplus 11", "oneplus 11r",
            "oneplus nord", "oneplus nord n30", "oneplus nord n300", "oneplus nord ce",
            "oneplus open", "oneplus fold", "oneplus ace", "oneplus 10 pro", "oneplus 10t",
            "oneplus phone", "oneplus deals", "oneplus trade in"
        ],
        "xiaomi": [
            "xiaomi", "redmi", "poco", "xiaomi 14", "xiaomi 13", "xiaomi 12",
            "redmi note", "redmi note 13", "redmi note 12", "poco f5", "poco x5",
            "mi phone", "xiaomi phone", "xiaomi deals"
        ],
        "nothing": [
            "nothing phone", "nothing phone 2", "nothing phone 2a", "nothing phone 1",
            "nothing ear", "carl pei phone", "nothing deals"
        ],
        "tcl": [
            "tcl phone", "tcl 50", "tcl 40", "tcl 30", "tcl stylus", "tcl smartphone"
        ],
        "budget": [
            "cheap phone", "budget phone", "phones under 100", "phones under 200",
            "phones under 300", "phones under 400", "phones under 500", "phones under 600",
            "affordable phone", "best budget phone", "cheap android", "budget android",
            "free phone", "free government phone", "lifeline phone", "acp phone",
            "best phone under 200", "best phone under 300", "best phone under 500",
            "cheap 5g phone", "budget 5g phone", "inexpensive phone", "low cost phone"
        ],
        "premium": [
            "best phone", "flagship phone", "premium phone", "top phone", "best smartphone",
            "high end phone", "luxury phone", "best android phone", "best camera phone",
            "best gaming phone", "best battery phone", "best phone 2024", "best phone 2025"
        ],
        "categories": [
            "flip phone", "foldable phone", "basic phone", "feature phone", "dumb phone",
            "senior phone", "senior cell phone", "jitterbug", "lively phone", "easy phone",
            "kids phone", "child phone", "kid friendly phone", "kids smartwatch",
            "rugged phone", "waterproof phone", "durable phone", "construction phone",
            "5g phone", "5g smartphone", "best 5g phone", "cheap 5g phone",
            "android phone", "smartphone", "cell phone", "mobile phone", "wireless phone"
        ],
        "accessories": [
            "phone case", "screen protector", "phone charger", "wireless charger",
            "car charger", "phone mount", "phone stand", "phone holder", "pop socket",
            "phone grip", "phone wallet", "mophie", "anker charger", "belkin charger"
        ],
        "other_brands": [
            "nokia", "nokia phone", "lg phone", "zte", "zte phone", "blu phone",
            "huawei", "honor", "oppo", "vivo", "realme", "asus phone", "rog phone",
            "sony xperia", "blackberry", "palm phone", "cat phone", "kyocera"
        ]
    }

    # Plan types - Massively Expanded
    PLAN_TYPES = [
        # Contract types
        "prepaid", "postpaid", "no contract", "contract", "pay as you go", "month to month",
        "byod", "bring your own device", "bring your own phone", "sim only", "esim only",
        # Data plans
        "unlimited", "unlimited data", "unlimited everything", "unlimited talk text data",
        "limited data", "metered", "data only", "data plan", "cheap data plan",
        "1gb", "2gb", "3gb", "4gb", "5gb", "10gb", "15gb", "20gb", "25gb", "30gb", "50gb", "100gb",
        "unlimited premium data", "unlimited plus", "unlimited starter", "unlimited welcome",
        # Line types
        "shared", "family", "family plan", "single line", "single", "multi line", "multiline",
        "2 lines", "3 lines", "4 lines", "5 lines", "2 line plan", "3 line plan", "4 line plan", "5 line plan",
        "add a line", "additional line", "extra line", "second line",
        # Business
        "business", "business plan", "enterprise", "small business", "smb", "corporate",
        "fleet", "fleet plan", "company phone", "work phone", "mdm",
        # Demographics - Expanded
        "student", "student plan", "college student", "student discount", "edu discount",
        "senior", "senior plan", "55+", "55 plus", "65+", "65 plus", "aarp", "aarp plan",
        "medicare", "senior discount", "senior cell phone plan", "easy plan",
        "military", "military plan", "military discount", "active duty", "veteran", "veterans",
        "first responder", "first responders", "nurse", "nurse discount", "healthcare worker",
        "teacher", "teacher plan", "teacher discount", "educator", "education discount",
        "government employee", "government", "federal employee", "state employee",
        # Special plans
        "international", "international plan", "international calling", "global plan",
        "travel", "travel plan", "cruise", "cruise plan", "international roaming",
        "hotspot only", "hotspot plan", "mobile hotspot", "mifi", "jetpack",
        "tablet plan", "tablet data", "ipad plan", "android tablet plan",
        "smartwatch plan", "watch plan", "apple watch plan", "galaxy watch plan",
        "connected device", "iot", "iot plan", "connected car", "wearable plan",
        # Affordable connectivity
        "low income", "lifeline", "acp", "affordable connectivity program", "ebt",
        "government phone", "free government phone", "safelink", "assurance wireless"
    ]

    # Data amounts
    DATA_AMOUNTS = [
        "1gb", "2gb", "3gb", "5gb", "10gb", "15gb", "20gb", "25gb", "50gb",
        "unlimited data", "unlimited premium", "unlimited plus", "unlimited starter"
    ]

    # Intent modifiers
    INTENT_MODIFIERS = {
        "transactional": ["buy", "purchase", "order", "get", "sign up", "subscribe", "activate",
                         "switch to", "port to", "upgrade to", "trade in"],
        "commercial": ["best", "top", "cheapest", "affordable", "budget", "premium",
                       "compare", "vs", "versus", "review", "rating", "deals", "offers",
                       "discount", "promo", "coupon", "sale", "black friday", "cyber monday"],
        "informational": ["what is", "how to", "guide", "explained", "tutorial", "learn",
                          "difference between", "pros and cons", "worth it", "should i"],
        "local": ["near me", "in my area", "nearby", "closest", "local"],
        "support": ["customer service", "help", "support", "contact", "phone number",
                    "live chat", "cancel", "return", "refund", "complaint"]
    }

    # Features - Expanded
    FEATURES = [
        # Network
        "5g", "5g ultra wideband", "5g uw", "5g nationwide", "4g lte", "4g", "lte",
        # Hotspot
        "hotspot", "mobile hotspot", "tethering", "personal hotspot", "hotspot data",
        # Calling
        "wifi calling", "hd voice", "volte", "international calling", "roaming",
        "unlimited talk", "unlimited text", "unlimited calls", "free calls",
        # Streaming
        "streaming", "hd streaming", "4k streaming", "music streaming", "video streaming",
        "netflix included", "hulu included", "disney plus", "apple tv plus",
        # Perks
        "cloud storage", "security", "insurance", "protection plan", "device protection",
        "apple one", "google one", "travel perks", "priority boarding",
        # Other
        "visual voicemail", "call filter", "spam blocking", "number share",
        "multi device", "family locator", "parental controls"
    ]

    # Internet services
    INTERNET_TYPES = [
        "fiber", "fiber optic", "gigabit", "cable", "dsl", "5g home", "fixed wireless",
        "satellite", "starlink", "broadband", "high speed"
    ]

    INTERNET_SPEEDS = [
        "100 mbps", "200 mbps", "300 mbps", "500 mbps", "1 gig", "2 gig",
        "fast", "fastest", "slow", "speed test"
    ]

    # Actions
    ACTIONS = [
        "buy", "get", "find", "compare", "check", "see", "view", "search",
        "switch", "change", "upgrade", "downgrade", "cancel", "activate",
        "setup", "configure", "troubleshoot", "fix", "reset"
    ]

    # Questions
    QUESTIONS = [
        "what is", "how much is", "how to", "where to", "when to", "why",
        "which", "is there", "can i", "should i", "do i need"
    ]

    # Price related
    PRICE_TERMS = [
        "price", "cost", "pricing", "rates", "fee", "charge", "bill",
        "monthly", "per month", "per line", "cheap", "expensive", "affordable",
        "budget", "free", "discount", "deal"
    ]

    def __init__(self):
        self.keywords = []
        self.keyword_set = set()  # For deduplication

    def add_keyword(self, keyword: str, category: str, subcategory: str,
                    intent: str, commercial_score: int):
        """Add keyword if not duplicate"""
        keyword = keyword.lower().strip()
        keyword = re.sub(r'\s+', ' ', keyword)  # Normalize whitespace

        if keyword and keyword not in self.keyword_set and len(keyword) > 3:
            self.keyword_set.add(keyword)
            self.keywords.append({
                "keyword": keyword,
                "category": category,
                "subcategory": subcategory,
                "intent": intent,
                "commercial_score": commercial_score,
                "search_volume": 100,  # Default, can be updated with API
                "cpc": 1.0
            })

    def generate_carrier_keywords(self):
        """Generate carrier-specific keywords"""
        print("Generating carrier keywords...")

        for carrier in self.CARRIERS:
            # Basic carrier searches
            self.add_keyword(carrier, "Carriers", "General", "Navigational", 50)
            self.add_keyword(f"{carrier} plans", "Mobile Plans", "Carrier Plans", "Commercial", 75)
            self.add_keyword(f"{carrier} phone plans", "Mobile Plans", "Carrier Plans", "Commercial", 75)
            self.add_keyword(f"{carrier} deals", "Deals", "Carrier Deals", "Transactional", 85)
            self.add_keyword(f"{carrier} promotions", "Deals", "Carrier Deals", "Transactional", 80)

            # Plan types
            for plan_type in self.PLAN_TYPES[:10]:
                self.add_keyword(f"{carrier} {plan_type} plan", "Mobile Plans", plan_type.title(), "Commercial", 70)
                self.add_keyword(f"{carrier} {plan_type} plans", "Mobile Plans", plan_type.title(), "Commercial", 70)

            # Phone + carrier
            for brand, models in self.PHONES.items():
                for model in models[:3]:
                    self.add_keyword(f"{model} {carrier}", "Devices", brand.title(), "Commercial", 75)
                    self.add_keyword(f"{carrier} {model}", "Devices", brand.title(), "Commercial", 75)
                    self.add_keyword(f"{carrier} {model} deal", "Deals", "Phone Deals", "Transactional", 85)

            # Features
            for feature in self.FEATURES[:8]:
                self.add_keyword(f"{carrier} {feature}", "Features", feature.title(), "Informational", 45)
                self.add_keyword(f"{carrier} {feature} plan", "Mobile Plans", "Feature Plans", "Commercial", 65)

            # Support
            self.add_keyword(f"{carrier} customer service", "Support", "Customer Service", "Navigational", 35)
            self.add_keyword(f"{carrier} phone number", "Support", "Contact", "Navigational", 30)
            self.add_keyword(f"{carrier} store near me", "Support", "Stores", "Local", 70)
            self.add_keyword(f"{carrier} coverage map", "Coverage", "Coverage Maps", "Informational", 50)
            self.add_keyword(f"{carrier} coverage in my area", "Coverage", "Coverage Check", "Local", 60)

            # Pricing
            for price_term in self.PRICE_TERMS[:5]:
                self.add_keyword(f"{carrier} {price_term}", "Pricing", "Carrier Pricing", "Commercial", 70)

    def generate_phone_keywords(self):
        """Generate phone-specific keywords"""
        print("Generating phone keywords...")

        for brand, models in self.PHONES.items():
            for model in models:
                # Basic searches
                self.add_keyword(model, "Devices", brand.title(), "Navigational", 50)
                self.add_keyword(f"{model} price", "Devices", brand.title(), "Commercial", 80)
                self.add_keyword(f"{model} deals", "Devices", brand.title(), "Transactional", 85)
                self.add_keyword(f"{model} specs", "Devices", brand.title(), "Informational", 40)
                self.add_keyword(f"{model} review", "Devices", brand.title(), "Commercial", 65)
                self.add_keyword(f"{model} case", "Accessories", "Cases", "Commercial", 70)

                # Intent modifiers
                for intent_type, modifiers in self.INTENT_MODIFIERS.items():
                    score = {"transactional": 90, "commercial": 75, "informational": 40,
                             "local": 70, "support": 35}.get(intent_type, 50)
                    for modifier in modifiers[:5]:
                        self.add_keyword(f"{modifier} {model}", "Devices", brand.title(), intent_type.title(), score)

                # Comparisons
                for other_brand, other_models in self.PHONES.items():
                    if brand != other_brand:
                        for other_model in other_models[:2]:
                            self.add_keyword(f"{model} vs {other_model}", "Devices", "Comparisons", "Commercial", 70)

    def generate_plan_keywords(self):
        """Generate plan-specific keywords"""
        print("Generating plan keywords...")

        for plan_type in self.PLAN_TYPES:
            # Basic plan searches
            self.add_keyword(f"{plan_type} plan", "Mobile Plans", plan_type.title(), "Commercial", 70)
            self.add_keyword(f"{plan_type} plans", "Mobile Plans", plan_type.title(), "Commercial", 70)
            self.add_keyword(f"{plan_type} phone plan", "Mobile Plans", plan_type.title(), "Commercial", 70)
            self.add_keyword(f"best {plan_type} plan", "Mobile Plans", plan_type.title(), "Commercial", 75)
            self.add_keyword(f"cheap {plan_type} plan", "Mobile Plans", plan_type.title(), "Commercial", 80)
            self.add_keyword(f"{plan_type} plan deals", "Deals", "Plan Deals", "Transactional", 85)

            # Data combinations
            for data_amount in self.DATA_AMOUNTS:
                self.add_keyword(f"{plan_type} {data_amount} plan", "Mobile Plans", "Data Plans", "Commercial", 70)

            # Questions
            for question in self.QUESTIONS[:5]:
                self.add_keyword(f"{question} {plan_type} plan", "Mobile Plans", plan_type.title(), "Informational", 35)

    def generate_internet_keywords(self):
        """Generate internet service keywords"""
        print("Generating internet keywords...")

        for internet_type in self.INTERNET_TYPES:
            self.add_keyword(f"{internet_type} internet", "Internet", internet_type.title(), "Commercial", 70)
            self.add_keyword(f"{internet_type} internet plans", "Internet", internet_type.title(), "Commercial", 75)
            self.add_keyword(f"best {internet_type} internet", "Internet", internet_type.title(), "Commercial", 75)
            self.add_keyword(f"{internet_type} internet near me", "Internet", internet_type.title(), "Local", 75)
            self.add_keyword(f"{internet_type} internet price", "Internet", internet_type.title(), "Commercial", 80)
            self.add_keyword(f"{internet_type} availability", "Internet", "Availability", "Informational", 60)

            # Speed combinations
            for speed in self.INTERNET_SPEEDS[:5]:
                self.add_keyword(f"{internet_type} {speed}", "Internet", "Speeds", "Commercial", 65)

            # Carrier combinations
            for carrier in self.CARRIERS[:10]:
                self.add_keyword(f"{carrier} {internet_type}", "Internet", internet_type.title(), "Commercial", 70)

    def generate_feature_keywords(self):
        """Generate feature-specific keywords"""
        print("Generating feature keywords...")

        for feature in self.FEATURES:
            self.add_keyword(feature, "Features", feature.title(), "Informational", 40)
            self.add_keyword(f"{feature} plan", "Mobile Plans", "Feature Plans", "Commercial", 65)
            self.add_keyword(f"best {feature} plan", "Mobile Plans", "Feature Plans", "Commercial", 70)
            self.add_keyword(f"unlimited {feature}", "Mobile Plans", "Unlimited Plans", "Commercial", 70)
            self.add_keyword(f"how to use {feature}", "Support", "How To", "Informational", 30)
            self.add_keyword(f"what is {feature}", "Features", feature.title(), "Informational", 25)

            # Carrier + feature
            for carrier in self.CARRIERS[:15]:
                self.add_keyword(f"{carrier} {feature}", "Features", feature.title(), "Informational", 50)

    def generate_support_keywords(self):
        """Generate support-related keywords"""
        print("Generating support keywords...")

        support_topics = [
            "bill pay", "pay bill", "payment", "autopay", "auto pay",
            "login", "my account", "sign in", "password reset",
            "activation", "activate", "activate phone", "activate sim",
            "port number", "transfer number", "keep my number",
            "cancel", "cancellation", "return", "refund",
            "upgrade", "upgrade phone", "early upgrade",
            "insurance", "protection", "warranty", "claim",
            "coverage", "network", "signal", "no service"
        ]

        for topic in support_topics:
            self.add_keyword(topic, "Support", "Account Management", "Navigational", 40)

            for carrier in self.CARRIERS[:15]:
                self.add_keyword(f"{carrier} {topic}", "Support", "Carrier Support", "Navigational", 45)

    def generate_comparison_keywords(self):
        """Generate comparison keywords"""
        print("Generating comparison keywords...")

        # Carrier vs carrier
        for i, carrier1 in enumerate(self.CARRIERS[:15]):
            for carrier2 in self.CARRIERS[i+1:15]:
                self.add_keyword(f"{carrier1} vs {carrier2}", "Comparisons", "Carrier Comparisons", "Commercial", 70)
                self.add_keyword(f"{carrier1} or {carrier2}", "Comparisons", "Carrier Comparisons", "Commercial", 65)
                self.add_keyword(f"switch from {carrier1} to {carrier2}", "Switching", "Carrier Switch", "Transactional", 80)

        # Plan type comparisons
        for i, plan1 in enumerate(self.PLAN_TYPES[:8]):
            for plan2 in self.PLAN_TYPES[i+1:8]:
                self.add_keyword(f"{plan1} vs {plan2}", "Comparisons", "Plan Comparisons", "Commercial", 65)

    def generate_deal_keywords(self):
        """Generate deals and promotions keywords"""
        print("Generating deal keywords...")

        deal_terms = [
            "deal", "deals", "offer", "offers", "promotion", "promotions",
            "discount", "discounts", "sale", "coupon", "promo code",
            "black friday", "cyber monday", "holiday deals", "back to school"
        ]

        for deal_term in deal_terms:
            self.add_keyword(f"phone {deal_term}", "Deals", "Phone Deals", "Transactional", 85)
            self.add_keyword(f"cell phone {deal_term}", "Deals", "Phone Deals", "Transactional", 85)
            self.add_keyword(f"smartphone {deal_term}", "Deals", "Phone Deals", "Transactional", 85)
            self.add_keyword(f"plan {deal_term}", "Deals", "Plan Deals", "Transactional", 80)
            self.add_keyword(f"wireless {deal_term}", "Deals", "Wireless Deals", "Transactional", 80)

            for carrier in self.CARRIERS[:15]:
                self.add_keyword(f"{carrier} {deal_term}", "Deals", "Carrier Deals", "Transactional", 85)

            for brand, models in self.PHONES.items():
                for model in models[:3]:
                    self.add_keyword(f"{model} {deal_term}", "Deals", "Phone Deals", "Transactional", 90)

    def generate_location_keywords(self):
        """Generate location-based keywords"""
        print("Generating location keywords...")

        locations = ["near me", "in my area", "nearby", "closest"]

        # Major US cities
        cities = [
            "new york", "los angeles", "chicago", "houston", "phoenix", "philadelphia",
            "san antonio", "san diego", "dallas", "san jose", "austin", "jacksonville",
            "fort worth", "columbus", "charlotte", "san francisco", "indianapolis", "seattle",
            "denver", "washington dc", "boston", "el paso", "detroit", "nashville", "portland",
            "memphis", "oklahoma city", "las vegas", "louisville", "baltimore", "milwaukee",
            "albuquerque", "tucson", "fresno", "mesa", "sacramento", "atlanta", "kansas city",
            "colorado springs", "miami", "raleigh", "omaha", "long beach", "virginia beach",
            "oakland", "minneapolis", "tulsa", "tampa", "arlington", "new orleans"
        ]

        # US States
        states = [
            "california", "texas", "florida", "new york", "pennsylvania", "illinois",
            "ohio", "georgia", "north carolina", "michigan", "new jersey", "virginia",
            "washington", "arizona", "massachusetts", "tennessee", "indiana", "maryland",
            "missouri", "wisconsin", "colorado", "minnesota", "south carolina", "alabama",
            "louisiana", "kentucky", "oregon", "oklahoma", "connecticut", "utah", "iowa",
            "nevada", "arkansas", "mississippi", "kansas", "new mexico", "nebraska",
            "idaho", "west virginia", "hawaii", "new hampshire", "maine", "montana",
            "rhode island", "delaware", "south dakota", "north dakota", "alaska",
            "vermont", "wyoming"
        ]

        for location in locations:
            self.add_keyword(f"phone store {location}", "Retail", "Stores", "Local", 75)
            self.add_keyword(f"cell phone store {location}", "Retail", "Stores", "Local", 75)
            self.add_keyword(f"wireless store {location}", "Retail", "Stores", "Local", 75)
            self.add_keyword(f"internet providers {location}", "Internet", "Local Providers", "Local", 80)
            self.add_keyword(f"5g coverage {location}", "Coverage", "5G Coverage", "Local", 65)
            self.add_keyword(f"cell coverage {location}", "Coverage", "Cell Coverage", "Local", 70)

            for carrier in self.CARRIERS[:15]:
                self.add_keyword(f"{carrier} store {location}", "Retail", "Carrier Stores", "Local", 75)
                self.add_keyword(f"{carrier} coverage {location}", "Coverage", "Carrier Coverage", "Local", 65)

        # City-based keywords
        for city in cities:
            self.add_keyword(f"best cell phone plans {city}", "Mobile Plans", "Local Plans", "Local", 70)
            self.add_keyword(f"internet providers {city}", "Internet", "Local Providers", "Local", 75)
            self.add_keyword(f"5g coverage {city}", "Coverage", "5G Coverage", "Local", 60)
            self.add_keyword(f"fiber internet {city}", "Internet", "Fiber", "Local", 70)
            self.add_keyword(f"phone stores {city}", "Retail", "Local Stores", "Local", 70)

            for carrier in self.CARRIERS[:10]:
                self.add_keyword(f"{carrier} {city}", "Carriers", "Local Coverage", "Local", 60)
                self.add_keyword(f"{carrier} store {city}", "Retail", "Carrier Stores", "Local", 70)

        # State-based keywords
        for state in states:
            self.add_keyword(f"best cell phone plans {state}", "Mobile Plans", "Local Plans", "Local", 65)
            self.add_keyword(f"internet providers {state}", "Internet", "Local Providers", "Local", 70)
            self.add_keyword(f"rural internet {state}", "Internet", "Rural Internet", "Local", 65)
            self.add_keyword(f"5g coverage {state}", "Coverage", "5G Coverage", "Local", 55)

            for carrier in self.CARRIERS[:8]:
                self.add_keyword(f"{carrier} coverage {state}", "Coverage", "Carrier Coverage", "Local", 55)

    def generate_question_keywords(self):
        """Generate question-based keywords"""
        print("Generating question keywords...")

        questions = {
            "what is": ["5g", "4g lte", "esim", "hotspot", "wifi calling", "unlimited data", "prepaid",
                       "mvno", "gsm", "cdma", "volte", "voip", "sim card", "imei", "unlock code",
                       "network lock", "carrier lock", "international roaming", "data throttling",
                       "deprioritization", "byod", "number porting", "mobile hotspot", "tethering"],
            "how to": ["activate phone", "unlock phone", "port number", "set up voicemail",
                       "check data usage", "pay bill", "cancel plan", "switch carriers",
                       "activate esim", "transfer esim", "remove sim card", "insert sim card",
                       "check coverage", "test signal", "improve signal", "boost signal",
                       "block spam calls", "stop robocalls", "enable wifi calling", "set up hotspot",
                       "add a line", "remove a line", "upgrade phone", "trade in phone",
                       "file insurance claim", "get unlock code", "check imei", "check compatibility",
                       "activate prepaid", "add data", "buy more data", "check balance"],
            "how much is": ["unlimited plan", "phone plan", "iphone", "galaxy", "internet",
                           "verizon", "att", "t-mobile", "mint mobile", "visible",
                           "family plan", "single line", "international plan", "hotspot"],
            "which is better": ["prepaid or postpaid", "5g or 4g", "iphone or samsung",
                               "verizon or att", "t-mobile or verizon", "att or t-mobile",
                               "mint or visible", "esim or physical sim", "contract or no contract"],
            "do i need": ["5g", "unlimited data", "hotspot", "insurance", "protection plan",
                         "international plan", "premium data", "tablet plan"],
            "why is": ["my phone slow", "my data slow", "5g not working", "wifi calling not working",
                      "my bill so high", "my signal weak", "my phone not connecting"],
            "can i": ["keep my number", "unlock my phone", "use my phone internationally",
                     "add a line", "cancel anytime", "switch carriers", "use esim",
                     "get unlimited data", "use my phone on any carrier"]
        }

        for question_start, topics in questions.items():
            for topic in topics:
                self.add_keyword(f"{question_start} {topic}", "FAQ", "Questions", "Informational", 30)
                # Add carrier-specific questions
                for carrier in self.CARRIERS[:20]:
                    self.add_keyword(f"{question_start} {carrier} {topic}", "FAQ", "Carrier Questions", "Informational", 35)

    def generate_price_keywords(self):
        """Generate price-focused keywords"""
        print("Generating price keywords...")

        price_ranges = [
            "under $10", "under $20", "under $25", "under $30", "under $40", "under $50",
            "under $60", "under $70", "under $80", "under $100", "under $150", "under $200",
            "$10", "$15", "$20", "$25", "$30", "$35", "$40", "$45", "$50", "$60", "$70", "$80",
            "10 dollars", "15 dollars", "20 dollars", "25 dollars", "30 dollars", "50 dollars",
            "cheapest", "most affordable", "best value", "budget friendly", "low cost"
        ]

        for price in price_ranges:
            self.add_keyword(f"phone plan {price}", "Pricing", "Price Search", "Commercial", 80)
            self.add_keyword(f"unlimited plan {price}", "Pricing", "Price Search", "Commercial", 80)
            self.add_keyword(f"cell phone plan {price}", "Pricing", "Price Search", "Commercial", 80)
            self.add_keyword(f"prepaid plan {price}", "Pricing", "Price Search", "Commercial", 75)
            self.add_keyword(f"family plan {price}", "Pricing", "Price Search", "Commercial", 75)
            self.add_keyword(f"{price} phone plan", "Pricing", "Price Search", "Commercial", 80)
            self.add_keyword(f"{price} per month", "Pricing", "Price Search", "Commercial", 70)
            self.add_keyword(f"{price} per line", "Pricing", "Price Search", "Commercial", 70)

    def generate_year_keywords(self):
        """Generate time-based keywords"""
        print("Generating year-based keywords...")

        years = ["2023", "2024", "2025", "2026"]
        time_modifiers = ["new", "latest", "newest", "current", "updated", "best"]

        topics = [
            "phone plans", "cell phone plans", "unlimited plans", "family plans",
            "prepaid plans", "5g phones", "iphone", "samsung galaxy", "best phones",
            "phone deals", "carrier deals", "black friday deals"
        ]

        for year in years:
            for topic in topics:
                self.add_keyword(f"{topic} {year}", "Trending", f"{year} Topics", "Commercial", 70)
                self.add_keyword(f"best {topic} {year}", "Trending", f"{year} Topics", "Commercial", 75)

        for modifier in time_modifiers:
            for topic in topics:
                self.add_keyword(f"{modifier} {topic}", "Trending", "Current Topics", "Commercial", 70)

    def generate_switching_keywords(self):
        """Generate carrier switching keywords"""
        print("Generating switching keywords...")

        switch_terms = ["switch from", "switch to", "change from", "change to",
                       "leave", "leaving", "port from", "port to", "transfer from",
                       "move from", "move to", "migrate from", "migrate to"]

        for carrier1 in self.CARRIERS[:25]:
            for carrier2 in self.CARRIERS[:25]:
                if carrier1 != carrier2:
                    for term in switch_terms[:3]:
                        self.add_keyword(f"{term} {carrier1} to {carrier2}", "Switching", "Carrier Switch", "Transactional", 85)

            # Generic switching
            self.add_keyword(f"switch to {carrier1}", "Switching", "Carrier Switch", "Transactional", 80)
            self.add_keyword(f"switch from {carrier1}", "Switching", "Carrier Switch", "Transactional", 80)
            self.add_keyword(f"leave {carrier1}", "Switching", "Carrier Switch", "Transactional", 75)
            self.add_keyword(f"leaving {carrier1}", "Switching", "Carrier Switch", "Transactional", 75)
            self.add_keyword(f"port to {carrier1}", "Switching", "Number Porting", "Transactional", 80)
            self.add_keyword(f"port number to {carrier1}", "Switching", "Number Porting", "Transactional", 80)
            self.add_keyword(f"{carrier1} switching bonus", "Deals", "Switch Deals", "Transactional", 85)
            self.add_keyword(f"{carrier1} trade in deal", "Deals", "Trade In", "Transactional", 85)

    def generate_accessories_keywords(self):
        """Generate phone accessories keywords"""
        print("Generating accessories keywords...")

        accessories = [
            "case", "cases", "cover", "screen protector", "tempered glass",
            "charger", "fast charger", "wireless charger", "charging cable", "usb c cable",
            "lightning cable", "car charger", "car mount", "phone holder", "phone stand",
            "earbuds", "wireless earbuds", "airpods", "galaxy buds", "headphones",
            "pop socket", "phone grip", "phone ring", "wallet case", "magsafe",
            "power bank", "portable charger", "battery case"
        ]

        for accessory in accessories:
            self.add_keyword(accessory, "Accessories", "General", "Commercial", 60)
            self.add_keyword(f"best {accessory}", "Accessories", "Best", "Commercial", 65)
            self.add_keyword(f"cheap {accessory}", "Accessories", "Budget", "Commercial", 70)

            # Phone-specific accessories
            for brand, models in self.PHONES.items():
                if brand in ["iphone", "samsung", "google"]:
                    for model in models[:5]:
                        self.add_keyword(f"{model} {accessory}", "Accessories", brand.title(), "Commercial", 70)

    def generate_sim_esim_keywords(self):
        """Generate SIM and eSIM related keywords"""
        print("Generating SIM/eSIM keywords...")

        sim_terms = [
            "sim card", "sim", "esim", "e-sim", "physical sim", "nano sim", "micro sim",
            "dual sim", "dual esim", "sim only", "sim free", "sim unlock"
        ]

        actions = ["buy", "get", "order", "activate", "setup", "transfer", "install", "remove"]

        for term in sim_terms:
            self.add_keyword(term, "SIM", "SIM Cards", "Commercial", 55)

            for action in actions:
                self.add_keyword(f"{action} {term}", "SIM", "SIM Actions", "Transactional", 65)
                self.add_keyword(f"how to {action} {term}", "SIM", "SIM How To", "Informational", 45)

            for carrier in self.CARRIERS[:25]:
                self.add_keyword(f"{carrier} {term}", "SIM", "Carrier SIM", "Commercial", 60)
                self.add_keyword(f"{term} for {carrier}", "SIM", "Carrier SIM", "Commercial", 60)

    def generate_network_coverage_keywords(self):
        """Generate network and coverage keywords"""
        print("Generating network coverage keywords...")

        coverage_terms = [
            "coverage", "coverage map", "signal", "signal strength", "network",
            "5g coverage", "4g coverage", "lte coverage", "reception", "bars",
            "dead zone", "no signal", "poor signal", "weak signal", "best coverage"
        ]

        for term in coverage_terms:
            self.add_keyword(term, "Coverage", "General", "Informational", 50)
            self.add_keyword(f"check {term}", "Coverage", "Coverage Check", "Informational", 55)

            for carrier in self.CARRIERS[:20]:
                self.add_keyword(f"{carrier} {term}", "Coverage", "Carrier Coverage", "Informational", 55)

    def generate_bundle_keywords(self):
        """Generate bundle and package deal keywords"""
        print("Generating bundle keywords...")

        bundles = [
            "bundle", "package", "combo", "package deal", "bundle deal",
            "phone and plan", "phone with plan", "phone plus plan",
            "internet and phone", "tv and internet", "triple play",
            "wireless and home internet", "mobile and home"
        ]

        for bundle in bundles:
            self.add_keyword(bundle, "Bundles", "Package Deals", "Commercial", 70)
            self.add_keyword(f"best {bundle}", "Bundles", "Package Deals", "Commercial", 75)
            self.add_keyword(f"cheap {bundle}", "Bundles", "Package Deals", "Commercial", 75)

            for carrier in self.CARRIERS[:15]:
                self.add_keyword(f"{carrier} {bundle}", "Bundles", "Carrier Bundles", "Commercial", 75)

    def generate_technical_keywords(self):
        """Generate technical specification keywords"""
        print("Generating technical keywords...")

        tech_terms = [
            "5g", "4g", "lte", "5g uw", "5g uc", "mmwave", "sub 6", "c band",
            "gsm", "cdma", "volte", "vonr", "hd voice", "wifi 6", "wifi 6e",
            "dual sim", "esim", "physical sim", "nano sim",
            "network bands", "band 71", "band 41", "band 14", "firstnet"
        ]

        for term in tech_terms:
            self.add_keyword(term, "Technology", "Network Tech", "Informational", 40)
            self.add_keyword(f"what is {term}", "Technology", "Tech Explainer", "Informational", 35)
            self.add_keyword(f"{term} explained", "Technology", "Tech Explainer", "Informational", 35)
            self.add_keyword(f"{term} phone", "Technology", "Tech Devices", "Commercial", 55)
            self.add_keyword(f"{term} compatible", "Technology", "Compatibility", "Informational", 50)

            for carrier in self.CARRIERS[:15]:
                self.add_keyword(f"{carrier} {term}", "Technology", "Carrier Tech", "Informational", 50)

    def generate_problem_solution_keywords(self):
        """Generate problem/troubleshooting keywords"""
        print("Generating problem/solution keywords...")

        problems = [
            "not working", "slow", "dropped calls", "no signal", "poor signal",
            "data not working", "can't connect", "won't connect", "keeps disconnecting",
            "battery drain", "overheating", "frozen", "stuck", "error",
            "won't charge", "not charging", "black screen", "won't turn on",
            "bill too high", "overcharged", "wrong bill", "billing error"
        ]

        solutions = [
            "fix", "solve", "troubleshoot", "repair", "help with",
            "how to fix", "solution for", "resolve", "what to do"
        ]

        devices = ["phone", "iphone", "samsung", "android", "5g", "service", "data", "hotspot"]

        for problem in problems:
            for device in devices:
                self.add_keyword(f"{device} {problem}", "Support", "Troubleshooting", "Informational", 40)

                for solution in solutions[:3]:
                    self.add_keyword(f"{solution} {device} {problem}", "Support", "Solutions", "Informational", 45)

    def generate_byod_keywords(self):
        """Generate bring your own device keywords"""
        print("Generating BYOD keywords...")

        byod_terms = [
            "bring your own phone", "bring your own device", "byod", "byop",
            "use my own phone", "keep my phone", "compatible phone",
            "phone compatibility", "will my phone work", "check compatibility",
            "imei check", "imei compatibility", "unlocked phone",
            "unlock phone", "carrier unlock", "sim unlock"
        ]

        for term in byod_terms:
            self.add_keyword(term, "BYOD", "Compatibility", "Informational", 55)

            for carrier in self.CARRIERS[:20]:
                self.add_keyword(f"{carrier} {term}", "BYOD", "Carrier BYOD", "Commercial", 60)
                self.add_keyword(f"{term} {carrier}", "BYOD", "Carrier BYOD", "Commercial", 60)

    def generate_streaming_perks_keywords(self):
        """Generate streaming and perks keywords"""
        print("Generating streaming/perks keywords...")

        streaming_services = [
            "netflix", "hulu", "disney plus", "disney+", "hbo max", "max",
            "amazon prime", "apple tv plus", "apple tv+", "peacock", "paramount plus",
            "youtube premium", "spotify", "apple music", "tidal"
        ]

        perks = [
            "free", "included", "included with", "bundled", "comes with",
            "get", "how to get", "activate"
        ]

        for service in streaming_services:
            self.add_keyword(f"{service} phone plan", "Perks", "Streaming", "Commercial", 65)
            self.add_keyword(f"phone plan with {service}", "Perks", "Streaming", "Commercial", 70)

            for perk in perks[:3]:
                self.add_keyword(f"{perk} {service}", "Perks", "Streaming Perks", "Commercial", 70)

            for carrier in self.CARRIERS[:15]:
                self.add_keyword(f"{carrier} {service}", "Perks", "Carrier Perks", "Commercial", 65)
                self.add_keyword(f"{carrier} free {service}", "Perks", "Carrier Perks", "Commercial", 70)

    def generate_payment_billing_keywords(self):
        """Generate payment and billing keywords"""
        print("Generating payment/billing keywords...")

        payment_terms = [
            "pay bill", "bill pay", "pay my bill", "payment", "make payment",
            "autopay", "auto pay", "automatic payment", "payment plan",
            "financing", "installment", "monthly payment", "pay later",
            "payment options", "credit check", "no credit check"
        ]

        billing_terms = [
            "bill", "billing", "statement", "invoice", "due date",
            "late fee", "early termination", "etf", "cancel fee"
        ]

        for term in payment_terms + billing_terms:
            self.add_keyword(term, "Billing", "Payments", "Navigational", 50)

            for carrier in self.CARRIERS[:20]:
                self.add_keyword(f"{carrier} {term}", "Billing", "Carrier Billing", "Navigational", 55)

    def generate_retail_store_keywords(self):
        """Generate retail and store location keywords"""
        print("Generating retail/store keywords...")

        store_terms = [
            "store", "store near me", "nearest store", "closest store",
            "store hours", "store locator", "find store", "retail store",
            "authorized dealer", "authorized retailer", "corporate store",
            "apple store", "best buy", "walmart", "costco", "target", "amazon"
        ]

        for term in store_terms:
            self.add_keyword(f"phone {term}", "Retail", "Stores", "Local", 70)
            self.add_keyword(f"cell phone {term}", "Retail", "Stores", "Local", 70)

            for carrier in self.CARRIERS[:20]:
                self.add_keyword(f"{carrier} {term}", "Retail", "Carrier Stores", "Local", 75)

    def generate_long_tail_combinations(self):
        """Generate long-tail keyword combinations"""
        print("Generating long-tail combinations...")

        # Carrier + Plan + Feature combinations
        for carrier in self.CARRIERS[:30]:
            for plan_type in self.PLAN_TYPES[:15]:
                for feature in self.FEATURES[:10]:
                    self.add_keyword(f"{carrier} {plan_type} with {feature}", "Mobile Plans", "Detailed Plans", "Commercial", 70)

        # Phone + Carrier + Action combinations
        for brand, models in self.PHONES.items():
            if brand in ["iphone", "samsung", "google"]:
                for model in models[:8]:
                    for carrier in self.CARRIERS[:15]:
                        for action in ["buy", "get", "deal on", "price for"]:
                            self.add_keyword(f"{action} {model} at {carrier}", "Devices", "Phone Deals", "Transactional", 80)
                            self.add_keyword(f"{model} on {carrier}", "Devices", "Carrier Phones", "Commercial", 70)

    def generate_promotional_keywords(self):
        """Generate promotional and seasonal keywords"""
        print("Generating promotional keywords...")

        events = [
            "black friday", "cyber monday", "prime day", "memorial day",
            "labor day", "presidents day", "fourth of july", "back to school",
            "christmas", "holiday", "new year", "valentines day",
            "spring sale", "summer sale", "fall sale", "winter sale"
        ]

        promo_types = ["deal", "deals", "sale", "sales", "offer", "offers",
                      "discount", "promo", "promotion", "special"]

        for event in events:
            for promo in promo_types[:4]:
                self.add_keyword(f"{event} phone {promo}", "Deals", "Seasonal", "Transactional", 85)
                self.add_keyword(f"{event} cell phone {promo}", "Deals", "Seasonal", "Transactional", 85)

                for carrier in self.CARRIERS[:15]:
                    self.add_keyword(f"{carrier} {event} {promo}", "Deals", "Carrier Seasonal", "Transactional", 90)

    def generate_trade_in_keywords(self):
        """Generate trade-in and upgrade keywords"""
        print("Generating trade-in keywords...")

        trade_terms = ["trade in", "trade-in", "tradein", "trade", "trade in value",
                      "trade in deal", "upgrade", "early upgrade", "phone upgrade"]

        for term in trade_terms:
            self.add_keyword(term, "Trade In", "General", "Transactional", 75)
            self.add_keyword(f"best {term}", "Trade In", "Best Deals", "Transactional", 80)

            for carrier in self.CARRIERS[:30]:
                self.add_keyword(f"{carrier} {term}", "Trade In", "Carrier Trade In", "Transactional", 80)

            for brand, models in self.PHONES.items():
                if brand in ["iphone", "samsung", "google", "motorola", "oneplus"]:
                    for model in models[:10]:
                        self.add_keyword(f"{model} {term}", "Trade In", "Phone Trade In", "Transactional", 80)
                        self.add_keyword(f"{term} {model}", "Trade In", "Phone Trade In", "Transactional", 80)

    def generate_app_service_keywords(self):
        """Generate app and service keywords"""
        print("Generating app/service keywords...")

        apps = [
            "my verizon", "my verizon app", "verizon app", "myat&t", "att app",
            "t-mobile app", "t-mobile tuesdays", "mint mobile app", "visible app",
            "carrier app", "mobile app", "account app", "bill pay app"
        ]

        services = [
            "spam filter", "call filter", "spam blocking", "robocall blocking",
            "caller id", "number lookup", "reverse phone lookup", "phone number search",
            "coverage check", "speed test", "data usage tracker", "family locator",
            "screen time", "parental controls", "content filter", "digital wellbeing"
        ]

        for app in apps:
            self.add_keyword(app, "Apps", "Carrier Apps", "Navigational", 50)
            self.add_keyword(f"download {app}", "Apps", "Carrier Apps", "Navigational", 55)

        for service in services:
            self.add_keyword(service, "Services", "Mobile Services", "Informational", 45)
            self.add_keyword(f"best {service}", "Services", "Mobile Services", "Commercial", 55)
            self.add_keyword(f"free {service}", "Services", "Mobile Services", "Commercial", 60)

            for carrier in self.CARRIERS[:20]:
                self.add_keyword(f"{carrier} {service}", "Services", "Carrier Services", "Informational", 50)

    def generate_international_keywords(self):
        """Generate international calling and roaming keywords"""
        print("Generating international keywords...")

        countries = [
            "mexico", "canada", "uk", "india", "china", "philippines", "germany",
            "france", "japan", "korea", "south korea", "brazil", "australia",
            "spain", "italy", "vietnam", "nigeria", "pakistan", "bangladesh",
            "egypt", "indonesia", "thailand", "colombia", "argentina"
        ]

        intl_terms = [
            "international calling", "international plan", "international roaming",
            "call", "calls to", "calling", "text", "data", "roaming", "travel to"
        ]

        for country in countries:
            self.add_keyword(f"call {country}", "International", "Calling", "Commercial", 65)
            self.add_keyword(f"calls to {country}", "International", "Calling", "Commercial", 65)
            self.add_keyword(f"calling {country}", "International", "Calling", "Commercial", 65)
            self.add_keyword(f"text {country}", "International", "Messaging", "Commercial", 60)
            self.add_keyword(f"{country} phone plan", "International", "Country Plans", "Commercial", 70)
            self.add_keyword(f"roaming in {country}", "International", "Roaming", "Informational", 55)
            self.add_keyword(f"phone service in {country}", "International", "Travel", "Commercial", 60)
            self.add_keyword(f"travel to {country} phone", "International", "Travel", "Commercial", 65)

            for carrier in self.CARRIERS[:15]:
                self.add_keyword(f"{carrier} {country}", "International", "Carrier International", "Commercial", 60)
                self.add_keyword(f"{carrier} calls to {country}", "International", "Carrier Calling", "Commercial", 65)

    def generate_unlocking_keywords(self):
        """Generate phone unlocking keywords"""
        print("Generating unlocking keywords...")

        unlock_terms = [
            "unlock", "unlocked", "unlocking", "carrier unlock", "network unlock",
            "sim unlock", "unlock code", "free unlock", "unlock service",
            "factory unlock", "permanent unlock", "imei unlock"
        ]

        for term in unlock_terms:
            self.add_keyword(term, "Unlocking", "General", "Transactional", 65)
            self.add_keyword(f"how to {term}", "Unlocking", "How To", "Informational", 55)
            self.add_keyword(f"free {term}", "Unlocking", "Free Unlock", "Commercial", 70)

            for carrier in self.CARRIERS[:30]:
                self.add_keyword(f"{carrier} {term}", "Unlocking", "Carrier Unlock", "Transactional", 70)
                self.add_keyword(f"{term} {carrier}", "Unlocking", "Carrier Unlock", "Transactional", 70)

            for brand, models in self.PHONES.items():
                if brand in ["iphone", "samsung", "google"]:
                    for model in models[:8]:
                        self.add_keyword(f"{term} {model}", "Unlocking", "Phone Unlock", "Transactional", 70)

    def generate_business_keywords(self):
        """Generate business and enterprise keywords"""
        print("Generating business keywords...")

        business_terms = [
            "business phone", "business plan", "business wireless", "corporate plan",
            "enterprise plan", "small business plan", "smb wireless", "company phone",
            "fleet management", "mdm", "mobile device management", "work phone",
            "business line", "second line", "business number", "work number"
        ]

        business_features = [
            "mobile hotspot", "international", "unlimited data", "priority support",
            "fleet tracking", "expense management", "corporate discount"
        ]

        for term in business_terms:
            self.add_keyword(term, "Business", "Business Plans", "Commercial", 70)
            self.add_keyword(f"best {term}", "Business", "Business Plans", "Commercial", 75)
            self.add_keyword(f"cheap {term}", "Business", "Business Plans", "Commercial", 75)

            for carrier in self.CARRIERS[:20]:
                self.add_keyword(f"{carrier} {term}", "Business", "Carrier Business", "Commercial", 75)

        for feature in business_features:
            self.add_keyword(f"business {feature}", "Business", "Business Features", "Commercial", 65)

    def generate_family_keywords(self):
        """Generate expanded family plan keywords"""
        print("Generating family keywords...")

        family_terms = [
            "family plan", "family plans", "family cell phone plan", "family mobile plan",
            "family wireless plan", "shared plan", "shared data plan", "multi line plan",
            "2 line family plan", "3 line family plan", "4 line family plan", "5 line family plan",
            "add family member", "add child to plan", "add parent to plan",
            "family locator", "family tracking", "family location sharing"
        ]

        for term in family_terms:
            self.add_keyword(term, "Family Plans", "General", "Commercial", 75)
            self.add_keyword(f"best {term}", "Family Plans", "Best Plans", "Commercial", 80)
            self.add_keyword(f"cheap {term}", "Family Plans", "Budget Plans", "Commercial", 80)
            self.add_keyword(f"cheapest {term}", "Family Plans", "Budget Plans", "Commercial", 80)

            for carrier in self.CARRIERS[:25]:
                self.add_keyword(f"{carrier} {term}", "Family Plans", "Carrier Family", "Commercial", 75)

    def generate_carrier_comparison_keywords(self):
        """Generate detailed carrier comparison keywords"""
        print("Generating carrier comparison keywords...")

        comparison_terms = [
            "vs", "versus", "or", "compared to", "comparison", "difference between",
            "better than", "cheaper than", "faster than"
        ]

        comparison_aspects = [
            "coverage", "price", "speed", "plans", "customer service", "network",
            "5g", "international", "family plan", "unlimited"
        ]

        for i, carrier1 in enumerate(self.CARRIERS[:20]):
            for carrier2 in self.CARRIERS[i+1:20]:
                for term in comparison_terms[:4]:
                    self.add_keyword(f"{carrier1} {term} {carrier2}", "Comparisons", "Carrier vs Carrier", "Commercial", 70)

                for aspect in comparison_aspects:
                    self.add_keyword(f"{carrier1} vs {carrier2} {aspect}", "Comparisons", "Detailed Comparison", "Commercial", 70)

    def generate_prepaid_postpaid_keywords(self):
        """Generate prepaid and postpaid specific keywords"""
        print("Generating prepaid/postpaid keywords...")

        prepaid_terms = [
            "prepaid phone", "prepaid plan", "prepaid wireless", "prepaid service",
            "pay as you go", "no contract phone", "no contract plan", "prepaid cell phone",
            "prepaid sim", "prepaid esim", "prepaid card", "refill", "refill card",
            "add minutes", "add data", "top up", "reload"
        ]

        postpaid_terms = [
            "postpaid plan", "contract plan", "monthly plan", "financed phone",
            "payment plan", "installment plan", "device payment", "phone financing"
        ]

        for term in prepaid_terms:
            self.add_keyword(term, "Prepaid", "General", "Commercial", 70)
            self.add_keyword(f"best {term}", "Prepaid", "Best Prepaid", "Commercial", 75)
            self.add_keyword(f"cheap {term}", "Prepaid", "Budget Prepaid", "Commercial", 75)

            for carrier in self.CARRIERS[:25]:
                self.add_keyword(f"{carrier} {term}", "Prepaid", "Carrier Prepaid", "Commercial", 70)

        for term in postpaid_terms:
            self.add_keyword(term, "Postpaid", "General", "Commercial", 65)
            self.add_keyword(f"best {term}", "Postpaid", "Best Postpaid", "Commercial", 70)

            for carrier in self.CARRIERS[:20]:
                self.add_keyword(f"{carrier} {term}", "Postpaid", "Carrier Postpaid", "Commercial", 70)

    def generate_data_speed_keywords(self):
        """Generate data and speed related keywords"""
        print("Generating data/speed keywords...")

        data_terms = [
            "data", "mobile data", "cellular data", "data usage", "data limit",
            "data cap", "unlimited data", "high speed data", "premium data",
            "deprioritization", "throttling", "data throttle", "slow data"
        ]

        speed_terms = [
            "fast", "fastest", "speed", "speeds", "download speed", "upload speed",
            "mbps", "gbps", "network speed", "5g speed", "lte speed"
        ]

        for term in data_terms:
            self.add_keyword(term, "Data", "General", "Informational", 50)
            self.add_keyword(f"check {term}", "Data", "Check Data", "Navigational", 55)
            self.add_keyword(f"how to {term}", "Data", "How To", "Informational", 45)

            for carrier in self.CARRIERS[:20]:
                self.add_keyword(f"{carrier} {term}", "Data", "Carrier Data", "Informational", 55)

        for term in speed_terms:
            self.add_keyword(f"phone {term}", "Speed", "General", "Informational", 50)
            self.add_keyword(f"mobile {term}", "Speed", "General", "Informational", 50)

            for carrier in self.CARRIERS[:20]:
                self.add_keyword(f"{carrier} {term}", "Speed", "Carrier Speed", "Informational", 55)

    def generate_mvno_keywords(self):
        """Generate MVNO-specific keywords"""
        print("Generating MVNO keywords...")

        mvno_terms = [
            "mvno", "mobile virtual network operator", "best mvno", "cheapest mvno",
            "mvno plans", "mvno vs major carrier", "what is mvno"
        ]

        mvno_networks = [
            "verizon mvno", "att mvno", "at&t mvno", "t-mobile mvno", "tmobile mvno",
            "verizon network", "att network", "t-mobile network"
        ]

        for term in mvno_terms:
            self.add_keyword(term, "MVNO", "General", "Informational", 55)

        for network in mvno_networks:
            self.add_keyword(network, "MVNO", "Network MVNOs", "Commercial", 60)
            self.add_keyword(f"best {network}", "MVNO", "Best MVNOs", "Commercial", 65)
            self.add_keyword(f"cheap {network}", "MVNO", "Budget MVNOs", "Commercial", 70)

    def generate_review_rating_keywords(self):
        """Generate review and rating keywords"""
        print("Generating review/rating keywords...")

        review_terms = [
            "review", "reviews", "rating", "ratings", "customer reviews",
            "user reviews", "honest review", "real review", "pros and cons",
            "worth it", "is it worth", "should i buy", "should i get"
        ]

        for term in review_terms:
            for carrier in self.CARRIERS[:25]:
                self.add_keyword(f"{carrier} {term}", "Reviews", "Carrier Reviews", "Commercial", 60)

            for brand, models in self.PHONES.items():
                if brand in ["iphone", "samsung", "google", "motorola"]:
                    for model in models[:8]:
                        self.add_keyword(f"{model} {term}", "Reviews", "Phone Reviews", "Commercial", 65)

    def generate_specific_use_case_keywords(self):
        """Generate specific use case keywords"""
        print("Generating use case keywords...")

        use_cases = [
            # User types
            "for seniors", "for students", "for kids", "for teens", "for travelers",
            "for international use", "for rural areas", "for gaming", "for streaming",
            # Situations
            "while traveling", "abroad", "overseas", "on vacation", "for work",
            "for small business", "for large family", "with bad credit", "no credit check",
            # Needs
            "with most data", "with best coverage", "with fastest speed",
            "with international calling", "with hotspot", "with no throttling"
        ]

        for use_case in use_cases:
            self.add_keyword(f"best phone {use_case}", "Use Cases", "Phone Use Cases", "Commercial", 70)
            self.add_keyword(f"best plan {use_case}", "Use Cases", "Plan Use Cases", "Commercial", 70)
            self.add_keyword(f"best carrier {use_case}", "Use Cases", "Carrier Use Cases", "Commercial", 70)
            self.add_keyword(f"phone plan {use_case}", "Use Cases", "Plan Use Cases", "Commercial", 65)
            self.add_keyword(f"cell phone plan {use_case}", "Use Cases", "Plan Use Cases", "Commercial", 65)

            for carrier in self.CARRIERS[:15]:
                self.add_keyword(f"{carrier} {use_case}", "Use Cases", "Carrier Use Cases", "Commercial", 60)

    def generate_phone_brand_combinations(self):
        """Generate exhaustive phone + carrier + action combinations"""
        print("Generating phone brand combinations...")

        actions = ["buy", "get", "order", "purchase", "find", "check price", "see deals", "compare"]
        descriptors = ["new", "used", "refurbished", "certified", "unlocked", "cheap", "best", "latest"]

        for brand, models in self.PHONES.items():
            if brand in ["iphone", "samsung", "google", "motorola", "oneplus"]:
                for model in models:
                    for carrier in self.CARRIERS[:40]:
                        self.add_keyword(f"{model} {carrier}", "Devices", "Carrier Phones", "Commercial", 70)
                        self.add_keyword(f"{carrier} {model}", "Devices", "Carrier Phones", "Commercial", 70)

                    for action in actions:
                        self.add_keyword(f"{action} {model}", "Devices", "Phone Purchase", "Transactional", 80)

                    for descriptor in descriptors:
                        self.add_keyword(f"{descriptor} {model}", "Devices", "Phone Search", "Commercial", 75)

    def generate_plan_pricing_matrix(self):
        """Generate plan + pricing combinations"""
        print("Generating plan pricing matrix...")

        plan_types = ["unlimited", "prepaid", "family", "single line", "business", "senior", "student", "military"]
        pricing = ["$15", "$20", "$25", "$30", "$35", "$40", "$50", "$60", "$70", "$80", "$100"]

        for plan in plan_types:
            for price in pricing:
                self.add_keyword(f"{plan} plan for {price}", "Pricing", "Plan Pricing", "Commercial", 75)
                self.add_keyword(f"{price} {plan} plan", "Pricing", "Plan Pricing", "Commercial", 75)
                self.add_keyword(f"{plan} plan under {price}", "Pricing", "Budget Plans", "Commercial", 80)
                self.add_keyword(f"best {plan} plan for {price}", "Pricing", "Best Price", "Commercial", 80)

                for carrier in self.CARRIERS[:20]:
                    self.add_keyword(f"{carrier} {plan} {price}", "Pricing", "Carrier Pricing", "Commercial", 75)

    def generate_feature_carrier_matrix(self):
        """Generate feature + carrier combinations"""
        print("Generating feature carrier matrix...")

        for feature in self.FEATURES:
            for carrier in self.CARRIERS[:40]:
                self.add_keyword(f"{carrier} {feature}", "Features", "Carrier Features", "Informational", 55)
                self.add_keyword(f"{feature} on {carrier}", "Features", "Carrier Features", "Informational", 55)
                self.add_keyword(f"{carrier} plan with {feature}", "Features", "Feature Plans", "Commercial", 65)
                self.add_keyword(f"does {carrier} have {feature}", "Features", "Feature Questions", "Informational", 45)

    def generate_location_carrier_matrix(self):
        """Generate location + carrier combinations with more cities"""
        print("Generating location carrier matrix...")

        # Expanded list of cities - top 150 US cities
        cities = [
            "new york", "los angeles", "chicago", "houston", "phoenix", "philadelphia",
            "san antonio", "san diego", "dallas", "san jose", "austin", "jacksonville",
            "fort worth", "columbus", "charlotte", "san francisco", "indianapolis", "seattle",
            "denver", "washington dc", "boston", "el paso", "detroit", "nashville", "portland",
            "memphis", "oklahoma city", "las vegas", "louisville", "baltimore", "milwaukee",
            "albuquerque", "tucson", "fresno", "mesa", "sacramento", "atlanta", "kansas city",
            "colorado springs", "miami", "raleigh", "omaha", "long beach", "virginia beach",
            "oakland", "minneapolis", "tulsa", "tampa", "arlington", "new orleans",
            "wichita", "cleveland", "bakersfield", "aurora", "anaheim", "honolulu", "santa ana",
            "riverside", "corpus christi", "lexington", "stockton", "henderson", "saint paul",
            "st louis", "cincinnati", "pittsburgh", "greensboro", "anchorage", "plano",
            "lincoln", "orlando", "irvine", "newark", "toledo", "durham", "chula vista",
            "fort wayne", "jersey city", "st petersburg", "laredo", "madison", "chandler",
            "buffalo", "lubbock", "scottsdale", "reno", "glendale", "gilbert", "winston salem",
            "north las vegas", "norfolk", "chesapeake", "garland", "irving", "hialeah",
            "fremont", "boise", "richmond", "baton rouge", "spokane", "des moines"
        ]

        for city in cities:
            for carrier in self.CARRIERS[:20]:
                self.add_keyword(f"{carrier} {city}", "Local", "City Coverage", "Local", 65)
                self.add_keyword(f"{carrier} coverage {city}", "Local", "City Coverage", "Local", 65)
                self.add_keyword(f"{carrier} store {city}", "Local", "City Stores", "Local", 70)
                self.add_keyword(f"{carrier} plans {city}", "Local", "City Plans", "Local", 65)

            self.add_keyword(f"best carrier {city}", "Local", "City Carriers", "Local", 70)
            self.add_keyword(f"best phone plan {city}", "Local", "City Plans", "Local", 70)
            self.add_keyword(f"cell phone stores {city}", "Local", "City Stores", "Local", 70)
            self.add_keyword(f"5g coverage {city}", "Local", "5G Coverage", "Local", 65)

    def generate_tablet_smartwatch_keywords(self):
        """Generate tablet and smartwatch plan keywords"""
        print("Generating tablet/smartwatch keywords...")

        devices = [
            "ipad", "ipad pro", "ipad air", "ipad mini", "galaxy tab", "surface",
            "android tablet", "samsung tablet", "amazon fire", "kindle",
            "apple watch", "apple watch ultra", "apple watch se", "galaxy watch",
            "galaxy watch 6", "pixel watch", "fitbit", "garmin", "smartwatch"
        ]

        for device in devices:
            self.add_keyword(f"{device} plan", "Connected Devices", "Device Plans", "Commercial", 65)
            self.add_keyword(f"{device} data plan", "Connected Devices", "Data Plans", "Commercial", 65)
            self.add_keyword(f"{device} cellular", "Connected Devices", "Cellular", "Commercial", 60)
            self.add_keyword(f"best {device} plan", "Connected Devices", "Best Plans", "Commercial", 70)
            self.add_keyword(f"cheap {device} plan", "Connected Devices", "Budget Plans", "Commercial", 70)

            for carrier in self.CARRIERS[:20]:
                self.add_keyword(f"{carrier} {device}", "Connected Devices", "Carrier Devices", "Commercial", 65)
                self.add_keyword(f"{carrier} {device} plan", "Connected Devices", "Carrier Plans", "Commercial", 70)

    def generate_home_internet_keywords(self):
        """Generate home internet keywords"""
        print("Generating home internet keywords...")

        internet_terms = [
            "home internet", "home wifi", "internet service", "internet provider",
            "broadband", "high speed internet", "fiber internet", "cable internet",
            "5g home internet", "fixed wireless", "rural internet", "satellite internet"
        ]

        speed_terms = ["100 mbps", "200 mbps", "300 mbps", "500 mbps", "1 gig", "gigabit", "fastest"]

        for term in internet_terms:
            self.add_keyword(term, "Home Internet", "General", "Commercial", 70)
            self.add_keyword(f"best {term}", "Home Internet", "Best Internet", "Commercial", 75)
            self.add_keyword(f"cheap {term}", "Home Internet", "Budget Internet", "Commercial", 75)
            self.add_keyword(f"{term} near me", "Home Internet", "Local Internet", "Local", 75)
            self.add_keyword(f"{term} in my area", "Home Internet", "Local Internet", "Local", 75)

            for carrier in self.CARRIERS[:20]:
                self.add_keyword(f"{carrier} {term}", "Home Internet", "Carrier Internet", "Commercial", 70)

            for speed in speed_terms:
                self.add_keyword(f"{term} {speed}", "Home Internet", "Speed Plans", "Commercial", 70)

    def generate_customer_service_keywords(self):
        """Generate customer service and support keywords"""
        print("Generating customer service keywords...")

        support_terms = [
            "customer service", "customer support", "phone number", "contact", "call",
            "live chat", "chat support", "help", "support number", "1800 number",
            "toll free", "hours", "support hours", "customer service hours"
        ]

        issues = [
            "billing issue", "payment problem", "refund", "cancel service", "dispute charge",
            "complaint", "file complaint", "escalate", "supervisor", "manager"
        ]

        for carrier in self.CARRIERS[:35]:
            for term in support_terms:
                self.add_keyword(f"{carrier} {term}", "Customer Service", "Carrier Support", "Navigational", 50)
            for issue in issues:
                self.add_keyword(f"{carrier} {issue}", "Customer Service", "Issue Resolution", "Navigational", 55)

    def generate_activation_setup_keywords(self):
        """Generate activation and setup keywords"""
        print("Generating activation/setup keywords...")

        activation_terms = [
            "activate", "activation", "activate phone", "activate sim", "activate esim",
            "activate new phone", "activate device", "setup", "set up", "configure",
            "first time setup", "initial setup", "get started"
        ]

        for term in activation_terms:
            self.add_keyword(term, "Activation", "General", "Navigational", 55)
            self.add_keyword(f"how to {term}", "Activation", "How To", "Informational", 50)

            for carrier in self.CARRIERS[:30]:
                self.add_keyword(f"{carrier} {term}", "Activation", "Carrier Activation", "Navigational", 60)
                self.add_keyword(f"how to {term} {carrier}", "Activation", "Carrier Setup", "Informational", 55)

            for brand, models in self.PHONES.items():
                if brand in ["iphone", "samsung", "google"]:
                    for model in models[:5]:
                        self.add_keyword(f"{term} {model}", "Activation", "Phone Activation", "Navigational", 55)

    def generate_all(self) -> List[Dict]:
        """Generate all keyword variations"""
        print("Starting comprehensive keyword generation...")
        print("-" * 50)

        # Core generation methods
        self.generate_carrier_keywords()
        self.generate_phone_keywords()
        self.generate_plan_keywords()
        self.generate_internet_keywords()
        self.generate_feature_keywords()
        self.generate_support_keywords()
        self.generate_comparison_keywords()
        self.generate_deal_keywords()
        self.generate_location_keywords()
        self.generate_question_keywords()

        # Additional generation methods for 100K target
        self.generate_price_keywords()
        self.generate_year_keywords()
        self.generate_switching_keywords()
        self.generate_accessories_keywords()
        self.generate_sim_esim_keywords()
        self.generate_network_coverage_keywords()
        self.generate_bundle_keywords()
        self.generate_technical_keywords()
        self.generate_problem_solution_keywords()
        self.generate_byod_keywords()
        self.generate_streaming_perks_keywords()
        self.generate_payment_billing_keywords()
        self.generate_retail_store_keywords()
        self.generate_long_tail_combinations()
        self.generate_promotional_keywords()

        # New generation methods to reach 100K
        self.generate_trade_in_keywords()
        self.generate_app_service_keywords()
        self.generate_international_keywords()
        self.generate_unlocking_keywords()
        self.generate_business_keywords()
        self.generate_family_keywords()
        self.generate_carrier_comparison_keywords()
        self.generate_prepaid_postpaid_keywords()
        self.generate_data_speed_keywords()
        self.generate_mvno_keywords()
        self.generate_review_rating_keywords()
        self.generate_specific_use_case_keywords()

        # Final batch - matrix generation to push to 100K
        self.generate_phone_brand_combinations()
        self.generate_plan_pricing_matrix()
        self.generate_feature_carrier_matrix()
        self.generate_location_carrier_matrix()
        self.generate_tablet_smartwatch_keywords()
        self.generate_home_internet_keywords()
        self.generate_customer_service_keywords()
        self.generate_activation_setup_keywords()

        print("-" * 50)
        print(f"Total unique keywords generated: {len(self.keywords)}")
        return self.keywords

    def build_taxonomy(self) -> Dict:
        """Build taxonomy structure from generated keywords"""
        # Group keywords by category and subcategory
        taxonomy = {
            "classification_system": {
                "version": "2.0",
                "industry": "telecommunications",
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
                "total_keywords": len(self.keywords),
                "total_topics": 0,
                "description": "Comprehensive telecom classification with 100K+ keywords"
            },
            "taxonomy": {
                "L1_categories": []
            }
        }

        # Group by category
        categories = {}
        for kw in self.keywords:
            cat = kw["category"]
            subcat = kw["subcategory"]
            intent = kw["intent"]

            if cat not in categories:
                categories[cat] = {}
            if subcat not in categories[cat]:
                categories[cat][subcat] = {}
            if intent not in categories[cat][subcat]:
                categories[cat][subcat][intent] = []

            categories[cat][subcat][intent].append(kw)

        # Build L1-L5 structure
        l1_id = 1
        topic_count = 0

        for cat_name, subcats in categories.items():
            l1_entry = {
                "id": f"L1_{str(l1_id).zfill(3)}",
                "name": cat_name,
                "slug": cat_name.lower().replace(" ", "-").replace("&", "and"),
                "L2_subcategories": []
            }

            l2_id = 1
            for subcat_name, intents in subcats.items():
                l2_entry = {
                    "id": f"L2_{str(l1_id).zfill(3)}_{str(l2_id).zfill(3)}",
                    "name": subcat_name,
                    "slug": subcat_name.lower().replace(" ", "-"),
                    "L3_intents": []
                }

                l3_id = 1
                for intent_name, keywords in intents.items():
                    # Group keywords into topics of 10
                    topics = []
                    for i in range(0, len(keywords), 10):
                        topic_batch = keywords[i:i+10]
                        if topic_batch:
                            topic_name = topic_batch[0]["keyword"].title()[:50]
                            topic_count += 1

                            l5_keywords = []
                            for j, kw in enumerate(topic_batch):
                                l5_keywords.append({
                                    "id": f"L5_{topic_count}_{j}",
                                    "keyword": kw["keyword"],
                                    "search_volume": kw["search_volume"],
                                    "cpc": kw["cpc"],
                                    "intent_score": kw["commercial_score"]
                                })

                            topics.append({
                                "id": f"L4_{topic_count}",
                                "topic": topic_name,
                                "slug": topic_name.lower().replace(" ", "-")[:30],
                                "L5_keywords": l5_keywords
                            })

                    if topics:
                        avg_score = sum(kw["commercial_score"] for kw in keywords) // len(keywords)
                        l3_entry = {
                            "id": f"L3_{l1_id}_{l2_id}_{l3_id}",
                            "intent_category": intent_name,
                            "commercial_score": avg_score,
                            "funnel_stage": self._get_funnel_stage(intent_name),
                            "L4_topics": topics
                        }
                        l2_entry["L3_intents"].append(l3_entry)
                        l3_id += 1

                if l2_entry["L3_intents"]:
                    l1_entry["L2_subcategories"].append(l2_entry)
                    l2_id += 1

            if l1_entry["L2_subcategories"]:
                taxonomy["taxonomy"]["L1_categories"].append(l1_entry)
                l1_id += 1

        taxonomy["classification_system"]["total_topics"] = topic_count
        return taxonomy

    def _get_funnel_stage(self, intent: str) -> str:
        """Map intent to funnel stage"""
        mapping = {
            "Transactional": "Purchase",
            "Commercial": "Consideration",
            "Informational": "Awareness",
            "Navigational": "Navigation",
            "Local": "Decision",
            "Support": "Retention"
        }
        return mapping.get(intent, "Awareness")

    def save(self, filepath: str):
        """Save to JSON file"""
        taxonomy = self.build_taxonomy()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(taxonomy, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(self.keywords)} keywords to {filepath}")
        return taxonomy


def main():
    expander = TelecomKeywordExpander()
    expander.generate_all()
    taxonomy = expander.save("telecom-classification-100K.json")

    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total Keywords: {taxonomy['classification_system']['total_keywords']}")
    print(f"Total Topics: {taxonomy['classification_system']['total_topics']}")
    print(f"Categories (L1): {len(taxonomy['taxonomy']['L1_categories'])}")

    # Show category breakdown
    print("\nKeywords by Category:")
    for l1 in taxonomy['taxonomy']['L1_categories']:
        kw_count = sum(
            len(l5["L5_keywords"])
            for l2 in l1["L2_subcategories"]
            for l3 in l2["L3_intents"]
            for l5 in l3["L4_topics"]
        )
        print(f"  {l1['name']}: {kw_count}")


if __name__ == "__main__":
    main()
