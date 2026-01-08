#!/usr/bin/env python3
"""
Generate a 10,000 keyword sample dataset for testing
This creates a balanced dataset across all categories with brand detection support
"""

import json
import os
from datetime import datetime
from collections import defaultdict


def generate_10k_sample():
    """Generate a 10,000 keyword sample dataset"""

    print("=" * 80)
    print("GENERATING 10K SAMPLE KEYWORD DATASET")
    print("=" * 80)

    # Define carriers (expanded list matching telecom_classifier.py)
    carriers = [
        # Big 3
        'verizon', 'at&t', 'att', 't-mobile', 'tmobile', 'sprint',
        # Prepaid
        'metro', 'cricket', 'boost', 'visible', 'mint mobile', 'mint',
        'us cellular', 'us mobile',
        # MVNOs
        'google fi', 'xfinity mobile', 'spectrum mobile', 'straight talk',
        'total wireless', 'tracfone', 'simple mobile', 'h2o wireless',
        'republic wireless', 'ting', 'consumer cellular', 'red pocket',
        'ultra mobile', 'tello', 'net10', 'lycamobile', 'hello mobile'
    ]

    # Define phone brands (expanded list)
    phones = {
        'iphone': ['iphone', 'iphone 16', 'iphone 16 pro', 'iphone 16 pro max',
                   'iphone 15', 'iphone 15 pro', 'iphone 14', 'iphone se'],
        'samsung': ['samsung', 'galaxy', 'galaxy s24', 'galaxy s24 ultra',
                    'galaxy s23', 'galaxy z flip', 'galaxy z fold', 'galaxy a54'],
        'google': ['pixel', 'google pixel', 'pixel 9', 'pixel 9 pro', 'pixel 8', 'pixel 8a'],
        'motorola': ['motorola', 'moto', 'moto g', 'moto g power', 'razr'],
        'oneplus': ['oneplus', 'oneplus 12', 'oneplus nord', 'oneplus open'],
        'other': ['nokia', 'tcl', 'nothing phone', 'xiaomi', 'redmi']
    }

    # Plan types
    plan_types = [
        'unlimited', 'prepaid', 'postpaid', 'family plan', 'single line',
        'budget plan', 'premium plan', 'student plan', 'senior plan',
        'military plan', 'business plan', '5g plan', 'data plan'
    ]

    # Features
    features = [
        'hotspot', 'unlimited data', '5g', 'wifi calling', 'international',
        'streaming', 'netflix', 'hulu', 'disney+', 'hbo max', 'apple music'
    ]

    # Actions
    actions = ['buy', 'get', 'compare', 'review', 'price', 'deal', 'switch to', 'upgrade']

    # Cities for local keywords
    cities = [
        'new york', 'los angeles', 'chicago', 'houston', 'phoenix',
        'philadelphia', 'san antonio', 'san diego', 'dallas', 'austin',
        'miami', 'atlanta', 'boston', 'seattle', 'denver', 'detroit'
    ]

    keywords = {}
    keyword_count = 0

    # Category definitions with target counts
    categories = {
        'Mobile Plans': {'target': 1500, 'keywords': []},
        'Devices': {'target': 2000, 'keywords': []},
        'Deals': {'target': 800, 'keywords': []},
        'Coverage': {'target': 500, 'keywords': []},
        'Comparisons': {'target': 600, 'keywords': []},
        'Customer Service': {'target': 400, 'keywords': []},
        'Switching': {'target': 500, 'keywords': []},
        'Trade In': {'target': 400, 'keywords': []},
        'Reviews': {'target': 500, 'keywords': []},
        'Local': {'target': 600, 'keywords': []},
        'Accessories': {'target': 400, 'keywords': []},
        'SIM': {'target': 300, 'keywords': []},
        'Unlocking': {'target': 300, 'keywords': []},
        'International': {'target': 300, 'keywords': []},
        'Connected Devices': {'target': 300, 'keywords': []},
        'Family Plans': {'target': 400, 'keywords': []},
        'Pricing': {'target': 400, 'keywords': []},
        'Features': {'target': 500, 'keywords': []},
        'Support': {'target': 300, 'keywords': []},
        'FAQ': {'target': 200, 'keywords': []},
    }

    def add_keyword(kw, category, subcategory, intent, score):
        nonlocal keyword_count
        kw = kw.lower().strip()
        if kw and kw not in keywords and len(categories[category]['keywords']) < categories[category]['target']:
            keywords[kw] = {
                'keyword': kw,
                'category': category,
                'subcategory': subcategory,
                'intent': intent,
                'score': score
            }
            categories[category]['keywords'].append(kw)
            keyword_count += 1

    print("\nGenerating keywords by category...")

    # 1. Mobile Plans (1500)
    print("  Generating Mobile Plans...")
    for carrier in carriers:
        for plan in plan_types:
            add_keyword(f"{carrier} {plan}", "Mobile Plans", "Carrier Plans", "Commercial", 75)
            add_keyword(f"best {carrier} {plan}", "Mobile Plans", "Best Plans", "Commercial", 80)
        add_keyword(f"{carrier} plans", "Mobile Plans", "Carrier Plans", "Commercial", 70)
        add_keyword(f"{carrier} unlimited", "Mobile Plans", "Unlimited", "Commercial", 75)
    for plan in plan_types:
        add_keyword(f"best {plan}", "Mobile Plans", "Best Plans", "Commercial", 75)
        add_keyword(f"cheap {plan}", "Mobile Plans", "Budget Plans", "Commercial", 80)
        add_keyword(f"cheapest {plan}", "Mobile Plans", "Budget Plans", "Commercial", 80)

    # 2. Devices (2000)
    print("  Generating Devices...")
    for brand, models in phones.items():
        for model in models:
            add_keyword(model, "Devices", brand.title(), "Commercial", 70)
            add_keyword(f"buy {model}", "Devices", "Purchase", "Transactional", 85)
            add_keyword(f"{model} price", "Devices", "Pricing", "Commercial", 75)
            add_keyword(f"{model} deals", "Devices", "Deals", "Commercial", 80)
            add_keyword(f"new {model}", "Devices", "New Phones", "Commercial", 75)
            add_keyword(f"used {model}", "Devices", "Used Phones", "Commercial", 70)
            add_keyword(f"refurbished {model}", "Devices", "Refurbished", "Commercial", 70)
            add_keyword(f"unlocked {model}", "Devices", "Unlocked", "Commercial", 75)
            for carrier in carriers[:10]:
                add_keyword(f"{model} {carrier}", "Devices", "Carrier Phones", "Commercial", 75)
    add_keyword("best phone 2025", "Devices", "Best Phones", "Commercial", 80)
    add_keyword("best android phone", "Devices", "Best Phones", "Commercial", 80)
    add_keyword("best budget phone", "Devices", "Budget Phones", "Commercial", 80)
    add_keyword("cheap phone", "Devices", "Budget Phones", "Commercial", 75)
    add_keyword("cheap android phone", "Devices", "Budget Phones", "Commercial", 75)

    # 3. Deals (800)
    print("  Generating Deals...")
    events = ['black friday', 'cyber monday', 'memorial day', 'labor day', 'christmas']
    for carrier in carriers:
        add_keyword(f"{carrier} deals", "Deals", "Carrier Deals", "Transactional", 85)
        add_keyword(f"{carrier} phone deals", "Deals", "Phone Deals", "Transactional", 85)
        add_keyword(f"{carrier} promotions", "Deals", "Promotions", "Transactional", 80)
        for event in events:
            add_keyword(f"{carrier} {event} deals", "Deals", "Seasonal", "Transactional", 90)
    for event in events:
        add_keyword(f"{event} phone deals", "Deals", "Seasonal", "Transactional", 85)
        add_keyword(f"{event} cell phone deals", "Deals", "Seasonal", "Transactional", 85)

    # 4. Coverage (500)
    print("  Generating Coverage...")
    for carrier in carriers:
        add_keyword(f"{carrier} coverage", "Coverage", "Carrier Coverage", "Informational", 55)
        add_keyword(f"{carrier} coverage map", "Coverage", "Coverage Maps", "Informational", 55)
        add_keyword(f"{carrier} 5g coverage", "Coverage", "5G Coverage", "Informational", 60)
        add_keyword(f"{carrier} signal", "Coverage", "Signal", "Informational", 50)
    add_keyword("5g coverage near me", "Coverage", "5G Coverage", "Local", 65)
    add_keyword("best coverage", "Coverage", "Best Coverage", "Commercial", 60)
    add_keyword("cell coverage check", "Coverage", "Coverage Check", "Informational", 55)

    # 5. Comparisons (600)
    print("  Generating Comparisons...")
    major_carriers = ['verizon', 'att', 't-mobile', 'sprint', 'visible', 'mint mobile']
    for i, c1 in enumerate(major_carriers):
        for c2 in major_carriers[i+1:]:
            add_keyword(f"{c1} vs {c2}", "Comparisons", "Carrier vs Carrier", "Commercial", 70)
            add_keyword(f"{c1} versus {c2}", "Comparisons", "Carrier vs Carrier", "Commercial", 70)
            add_keyword(f"{c1} vs {c2} coverage", "Comparisons", "Coverage Comparison", "Commercial", 70)
            add_keyword(f"{c1} vs {c2} price", "Comparisons", "Price Comparison", "Commercial", 70)
    add_keyword("iphone vs samsung", "Comparisons", "Phone Comparison", "Commercial", 70)
    add_keyword("iphone vs pixel", "Comparisons", "Phone Comparison", "Commercial", 70)
    add_keyword("prepaid vs postpaid", "Comparisons", "Plan Comparison", "Commercial", 65)

    # 6. Customer Service (400)
    print("  Generating Customer Service...")
    for carrier in carriers:
        add_keyword(f"{carrier} customer service", "Customer Service", "Carrier Support", "Navigational", 50)
        add_keyword(f"{carrier} customer service number", "Customer Service", "Phone Numbers", "Navigational", 55)
        add_keyword(f"{carrier} support", "Customer Service", "Carrier Support", "Navigational", 50)
        add_keyword(f"{carrier} phone number", "Customer Service", "Phone Numbers", "Navigational", 55)
        add_keyword(f"{carrier} contact", "Customer Service", "Contact", "Navigational", 50)
        add_keyword(f"{carrier} live chat", "Customer Service", "Live Chat", "Navigational", 55)

    # 7. Switching (500)
    print("  Generating Switching...")
    for carrier in carriers[:15]:
        add_keyword(f"switch to {carrier}", "Switching", "Carrier Switch", "Transactional", 80)
        add_keyword(f"switch from {carrier}", "Switching", "Carrier Switch", "Transactional", 80)
        add_keyword(f"leave {carrier}", "Switching", "Carrier Switch", "Transactional", 75)
        add_keyword(f"port to {carrier}", "Switching", "Number Porting", "Transactional", 80)
    for i, c1 in enumerate(carriers[:10]):
        for c2 in carriers[:10]:
            if c1 != c2:
                add_keyword(f"switch from {c1} to {c2}", "Switching", "Carrier Switch", "Transactional", 85)

    # 8. Trade In (400)
    print("  Generating Trade In...")
    for carrier in carriers[:15]:
        add_keyword(f"{carrier} trade in", "Trade In", "Carrier Trade In", "Transactional", 80)
        add_keyword(f"{carrier} trade in value", "Trade In", "Trade Values", "Commercial", 75)
        add_keyword(f"{carrier} trade in deal", "Trade In", "Trade Deals", "Transactional", 85)
    for brand, models in phones.items():
        for model in models[:3]:
            add_keyword(f"{model} trade in", "Trade In", "Phone Trade In", "Transactional", 80)
            add_keyword(f"{model} trade in value", "Trade In", "Trade Values", "Commercial", 75)

    # 9. Reviews (500)
    print("  Generating Reviews...")
    for carrier in carriers:
        add_keyword(f"{carrier} review", "Reviews", "Carrier Reviews", "Informational", 60)
        add_keyword(f"{carrier} reviews", "Reviews", "Carrier Reviews", "Informational", 60)
    for brand, models in phones.items():
        for model in models:
            add_keyword(f"{model} review", "Reviews", "Phone Reviews", "Informational", 65)
            add_keyword(f"{model} reviews", "Reviews", "Phone Reviews", "Informational", 65)

    # 10. Local (600)
    print("  Generating Local...")
    for city in cities:
        add_keyword(f"best phone plan {city}", "Local", "City Plans", "Local", 70)
        add_keyword(f"cell phone stores {city}", "Local", "City Stores", "Local", 70)
        add_keyword(f"5g coverage {city}", "Local", "City Coverage", "Local", 65)
        for carrier in carriers[:8]:
            add_keyword(f"{carrier} store {city}", "Local", "Carrier Stores", "Local", 75)
            add_keyword(f"{carrier} coverage {city}", "Local", "City Coverage", "Local", 65)

    # 11. Accessories (400)
    print("  Generating Accessories...")
    accessories = ['case', 'screen protector', 'charger', 'wireless charger', 'earbuds', 'cable']
    for brand, models in phones.items():
        for model in models[:4]:
            for accessory in accessories:
                add_keyword(f"{model} {accessory}", "Accessories", accessory.title(), "Commercial", 70)
    add_keyword("magsafe charger", "Accessories", "Chargers", "Commercial", 70)
    add_keyword("best airpods alternative", "Accessories", "Earbuds", "Commercial", 65)

    # 12. SIM (300)
    print("  Generating SIM...")
    sim_types = ['sim card', 'esim', 'nano sim', 'sim only']
    for sim in sim_types:
        add_keyword(sim, "SIM", "SIM Cards", "Commercial", 55)
        add_keyword(f"what is {sim}", "SIM", "SIM Info", "Informational", 45)
        for carrier in carriers[:10]:
            add_keyword(f"{carrier} {sim}", "SIM", "Carrier SIM", "Commercial", 60)

    # 13. Unlocking (300)
    print("  Generating Unlocking...")
    for carrier in carriers:
        add_keyword(f"unlock {carrier} phone", "Unlocking", "Carrier Unlock", "Transactional", 70)
        add_keyword(f"{carrier} unlock", "Unlocking", "Carrier Unlock", "Transactional", 70)
    for brand, models in phones.items():
        for model in models[:3]:
            add_keyword(f"unlock {model}", "Unlocking", "Phone Unlock", "Transactional", 70)

    # 14. International (300)
    print("  Generating International...")
    countries = ['mexico', 'canada', 'uk', 'india', 'china', 'philippines', 'germany', 'japan']
    for country in countries:
        add_keyword(f"call {country}", "International", "Calling", "Commercial", 65)
        add_keyword(f"roaming in {country}", "International", "Roaming", "Informational", 55)
        add_keyword(f"phone plan {country}", "International", "Travel Plans", "Commercial", 70)
    for carrier in carriers[:10]:
        add_keyword(f"{carrier} international plan", "International", "Carrier International", "Commercial", 65)
        add_keyword(f"{carrier} international calling", "International", "Carrier Calling", "Commercial", 65)

    # 15. Connected Devices (300)
    print("  Generating Connected Devices...")
    devices = ['ipad', 'apple watch', 'galaxy watch', 'tablet', 'smartwatch', 'pixel watch']
    for device in devices:
        add_keyword(f"{device} plan", "Connected Devices", "Device Plans", "Commercial", 65)
        add_keyword(f"{device} data plan", "Connected Devices", "Data Plans", "Commercial", 65)
        add_keyword(f"{device} cellular", "Connected Devices", "Cellular", "Commercial", 60)
        for carrier in carriers[:8]:
            add_keyword(f"{carrier} {device} plan", "Connected Devices", "Carrier Plans", "Commercial", 70)
    add_keyword("tablet cellular plan", "Connected Devices", "Data Plans", "Commercial", 65)

    # 16. Family Plans (400)
    print("  Generating Family Plans...")
    for carrier in carriers:
        add_keyword(f"{carrier} family plan", "Family Plans", "Carrier Family", "Commercial", 75)
    line_counts = ['2 line', '3 line', '4 line', '5 line']
    for lines in line_counts:
        add_keyword(f"{lines} family plan", "Family Plans", "Multi-Line", "Commercial", 75)
        add_keyword(f"best {lines} plan", "Family Plans", "Best Family", "Commercial", 80)

    # 17. Pricing (400)
    print("  Generating Pricing...")
    prices = ['$20', '$25', '$30', '$40', '$50', '$60', '$80', '$100']
    for price in prices:
        add_keyword(f"phone plan under {price}", "Pricing", "Budget Search", "Commercial", 80)
        add_keyword(f"unlimited plan under {price}", "Pricing", "Budget Search", "Commercial", 80)
        add_keyword(f"cell phone plan {price}", "Pricing", "Price Search", "Commercial", 75)

    # 18. Features (500)
    print("  Generating Features...")
    for feature in features:
        add_keyword(f"plan with {feature}", "Features", "Feature Plans", "Commercial", 65)
        add_keyword(f"best {feature} plan", "Features", "Best Features", "Commercial", 70)
        for carrier in carriers[:10]:
            add_keyword(f"{carrier} {feature}", "Features", "Carrier Features", "Informational", 55)
    add_keyword("unlimited hotspot plan", "Features", "Hotspot", "Commercial", 70)
    add_keyword("netflix included phone plan", "Features", "Streaming", "Commercial", 70)

    # 19. Support (300)
    print("  Generating Support...")
    issues = ['not working', 'slow', 'no signal', 'dropped calls', 'data not working']
    for issue in issues:
        add_keyword(f"phone {issue}", "Support", "Troubleshooting", "Informational", 40)
        add_keyword(f"fix phone {issue}", "Support", "Solutions", "Informational", 45)
    add_keyword("phone not connecting to network", "Support", "Troubleshooting", "Informational", 40)

    # 20. FAQ (200)
    print("  Generating FAQ...")
    questions = ['what is', 'how to', 'how much is', 'can i', 'do i need']
    topics = ['5g', 'esim', 'hotspot', 'wifi calling', 'unlimited data', 'prepaid']
    for q in questions:
        for topic in topics:
            add_keyword(f"{q} {topic}", "FAQ", "Questions", "Informational", 35)

    # Additional generation to reach 10K
    print("\n  Expanding to reach 10K target...")

    # More carrier + plan combinations
    print("    Adding carrier plan expansions...")
    plan_modifiers = ['best', 'cheap', 'cheapest', 'affordable', 'new', 'latest', '2025']
    for carrier in carriers:
        for modifier in plan_modifiers:
            for plan in plan_types:
                add_keyword(f"{modifier} {carrier} {plan}", "Mobile Plans", "Modified Plans", "Commercial", 75)

    # More phone model variations
    print("    Adding phone model expansions...")
    phone_modifiers = ['new', 'used', 'refurbished', 'certified', 'best', 'cheap', 'budget']
    colors = ['black', 'white', 'blue', 'pink', 'gold', 'silver', 'titanium']
    storage = ['128gb', '256gb', '512gb', '1tb']
    for brand, models in phones.items():
        for model in models:
            for color in colors[:3]:
                add_keyword(f"{model} {color}", "Devices", "Phone Colors", "Commercial", 70)
            for size in storage[:2]:
                add_keyword(f"{model} {size}", "Devices", "Storage Options", "Commercial", 70)
            for modifier in phone_modifiers:
                add_keyword(f"{modifier} {model}", "Devices", "Phone Search", "Commercial", 75)

    # More deal combinations
    print("    Adding deal expansions...")
    deal_types = ['sale', 'offer', 'promotion', 'discount', 'special', 'promo']
    for carrier in carriers:
        for deal in deal_types:
            add_keyword(f"{carrier} {deal}", "Deals", "Carrier Deals", "Transactional", 80)
        for brand, models in phones.items():
            for model in models[:2]:
                add_keyword(f"{carrier} {model} deal", "Deals", "Phone Deals", "Transactional", 85)

    # More comparison combinations
    print("    Adding comparison expansions...")
    compare_aspects = ['coverage', 'price', 'speed', '5g', 'plans', 'customer service', 'network']
    for i, c1 in enumerate(carriers[:20]):
        for c2 in carriers[i+1:20]:
            for aspect in compare_aspects:
                add_keyword(f"{c1} vs {c2} {aspect}", "Comparisons", "Detailed Comparison", "Commercial", 70)

    # More local combinations
    print("    Adding local expansions...")
    more_cities = ['san francisco', 'portland', 'nashville', 'orlando', 'charlotte', 'pittsburgh',
                   'indianapolis', 'columbus', 'milwaukee', 'kansas city', 'sacramento', 'las vegas',
                   'memphis', 'baltimore', 'oklahoma city', 'louisville', 'richmond', 'new orleans',
                   'tucson', 'fresno', 'mesa', 'omaha', 'colorado springs', 'raleigh', 'long beach']
    for city in more_cities:
        add_keyword(f"best carrier {city}", "Local", "City Carriers", "Local", 70)
        add_keyword(f"phone stores {city}", "Local", "City Stores", "Local", 70)
        add_keyword(f"internet providers {city}", "Local", "City Internet", "Local", 65)
        for carrier in carriers[:5]:
            add_keyword(f"{carrier} {city}", "Local", "Carrier Local", "Local", 65)

    # More feature combinations
    print("    Adding feature expansions...")
    more_features = ['roaming', 'caller id', 'voicemail', 'call forwarding', 'mobile hotspot',
                     'tethering', 'visual voicemail', 'hd voice', 'wifi', 'data rollover']
    for feature in more_features:
        add_keyword(f"plan with {feature}", "Features", "Feature Plans", "Commercial", 65)
        for carrier in carriers[:15]:
            add_keyword(f"{carrier} {feature}", "Features", "Carrier Features", "Informational", 55)

    # More switching combinations
    print("    Adding switching expansions...")
    switch_terms = ['switch', 'change', 'move', 'transfer', 'port', 'leave', 'quit', 'cancel']
    for term in switch_terms:
        for carrier in carriers[:15]:
            add_keyword(f"{term} to {carrier}", "Switching", "Carrier Switch", "Transactional", 80)
            add_keyword(f"{term} from {carrier}", "Switching", "Carrier Switch", "Transactional", 80)

    # More accessories
    print("    Adding accessory expansions...")
    more_accessories = ['stand', 'mount', 'holder', 'grip', 'wallet case', 'power bank',
                        'fast charger', 'car charger', 'magsafe', 'airpods', 'galaxy buds']
    for accessory in more_accessories:
        add_keyword(accessory, "Accessories", "General", "Commercial", 65)
        add_keyword(f"best {accessory}", "Accessories", "Best", "Commercial", 70)
        for brand, models in phones.items():
            for model in models[:2]:
                add_keyword(f"{model} {accessory}", "Accessories", brand.title(), "Commercial", 70)

    # More SIM keywords
    print("    Adding SIM expansions...")
    sim_actions = ['activate', 'setup', 'install', 'transfer', 'replace', 'order', 'buy']
    for action in sim_actions:
        for sim in sim_types:
            add_keyword(f"{action} {sim}", "SIM", "SIM Actions", "Transactional", 65)
            for carrier in carriers[:10]:
                add_keyword(f"{action} {carrier} {sim}", "SIM", "Carrier SIM", "Transactional", 65)

    # More unlocking combinations
    print("    Adding unlocking expansions...")
    for carrier in carriers:
        add_keyword(f"{carrier} unlock policy", "Unlocking", "Unlock Policy", "Informational", 55)
        add_keyword(f"{carrier} unlock code", "Unlocking", "Unlock Codes", "Transactional", 70)
        add_keyword(f"free {carrier} unlock", "Unlocking", "Free Unlock", "Commercial", 75)

    # More international keywords
    print("    Adding international expansions...")
    more_countries = ['france', 'spain', 'italy', 'australia', 'brazil', 'korea', 'vietnam',
                      'thailand', 'indonesia', 'nigeria', 'egypt', 'russia', 'turkey', 'ireland']
    intl_actions = ['call', 'text', 'data', 'roaming', 'travel', 'use phone']
    for country in more_countries:
        for action in intl_actions:
            add_keyword(f"{action} {country}", "International", "Country Actions", "Commercial", 65)
        for carrier in carriers[:8]:
            add_keyword(f"{carrier} {country}", "International", "Carrier International", "Commercial", 60)

    # More connected device combinations
    print("    Adding connected device expansions...")
    more_devices = ['android tablet', 'samsung tablet', 'kindle', 'fitbit', 'garmin',
                    'apple watch ultra', 'apple watch se', 'galaxy watch 6']
    for device in more_devices:
        add_keyword(f"{device} plan", "Connected Devices", "Device Plans", "Commercial", 65)
        add_keyword(f"best {device} plan", "Connected Devices", "Best Plans", "Commercial", 70)
        for carrier in carriers[:10]:
            add_keyword(f"{carrier} {device}", "Connected Devices", "Carrier Plans", "Commercial", 70)

    # More family plan keywords
    print("    Adding family plan expansions...")
    family_terms = ['shared plan', 'multi line', 'add a line', 'additional line', 'extra line']
    for term in family_terms:
        add_keyword(term, "Family Plans", "General", "Commercial", 70)
        add_keyword(f"best {term}", "Family Plans", "Best Family", "Commercial", 75)
        for carrier in carriers[:15]:
            add_keyword(f"{carrier} {term}", "Family Plans", "Carrier Family", "Commercial", 75)

    # More pricing keywords
    print("    Adding pricing expansions...")
    more_prices = ['$15', '$35', '$45', '$55', '$65', '$75', '$90', '$120']
    price_terms = ['under', 'around', 'about', 'less than', 'for']
    for price in more_prices:
        for term in price_terms:
            add_keyword(f"phone plan {term} {price}", "Pricing", "Price Search", "Commercial", 80)
            add_keyword(f"unlimited {term} {price}", "Pricing", "Unlimited Pricing", "Commercial", 80)

    # More support keywords
    print("    Adding support expansions...")
    more_issues = ['battery drain', 'overheating', 'screen frozen', 'apps crashing', 'wifi not working',
                   'bluetooth issues', 'charging problem', 'cant receive calls', 'cant make calls']
    for issue in more_issues:
        add_keyword(f"phone {issue}", "Support", "Troubleshooting", "Informational", 40)
        add_keyword(f"fix {issue}", "Support", "Solutions", "Informational", 45)
        add_keyword(f"help {issue}", "Support", "Help", "Informational", 40)

    # More FAQ keywords
    print("    Adding FAQ expansions...")
    more_questions = ['should i', 'is it worth', 'does', 'which is better', 'why is']
    more_topics = ['upgrade', 'switch carriers', 'get 5g', 'buy new phone', 'trade in', 'unlimited']
    for q in more_questions:
        for topic in more_topics:
            add_keyword(f"{q} {topic}", "FAQ", "Questions", "Informational", 35)
            for carrier in carriers[:5]:
                add_keyword(f"{q} {carrier} {topic}", "FAQ", "Carrier Questions", "Informational", 40)

    # Additional carrier-specific keywords to fill gaps
    print("    Adding carrier specific expansions...")
    carrier_terms = ['login', 'account', 'my account', 'app', 'rewards', 'perks', 'offers',
                     'number', 'hotline', 'headquarters', 'jobs', 'careers', 'bill pay']
    for carrier in carriers:
        for term in carrier_terms:
            add_keyword(f"{carrier} {term}", "Customer Service", "Carrier Services", "Navigational", 50)

    # Fill remaining gaps to reach 10K
    print("    Final expansion to reach 10K...")

    # More device-carrier combinations
    all_phones = []
    for brand, models in phones.items():
        all_phones.extend(models)
    for phone in all_phones:
        for carrier in carriers:
            add_keyword(f"{phone} on {carrier}", "Devices", "Carrier Phones", "Commercial", 70)
            add_keyword(f"get {phone} at {carrier}", "Devices", "Purchase", "Transactional", 80)

    # More coverage keywords
    coverage_terms = ['network', 'signal strength', 'reception', 'bars', 'dead zone', 'tower']
    for term in coverage_terms:
        add_keyword(term, "Coverage", "General", "Informational", 50)
        add_keyword(f"check {term}", "Coverage", "Check", "Informational", 55)
        for carrier in carriers[:15]:
            add_keyword(f"{carrier} {term}", "Coverage", "Carrier Coverage", "Informational", 55)

    # More trade-in keywords
    trade_terms = ['trade', 'trade-in', 'tradein', 'upgrade', 'swap', 'exchange']
    for term in trade_terms:
        add_keyword(f"best {term} deal", "Trade In", "Best Deals", "Transactional", 80)
        for carrier in carriers[:20]:
            add_keyword(f"{carrier} {term} offer", "Trade In", "Carrier Offers", "Transactional", 80)
            add_keyword(f"{carrier} phone {term}", "Trade In", "Phone Trade", "Transactional", 75)

    # More review keywords
    review_terms = ['rating', 'ratings', 'pros and cons', 'worth it', 'honest review', 'real review']
    for term in review_terms:
        for carrier in carriers[:15]:
            add_keyword(f"{carrier} {term}", "Reviews", "Carrier Reviews", "Informational", 60)
        for phone in all_phones[:15]:
            add_keyword(f"{phone} {term}", "Reviews", "Phone Reviews", "Informational", 65)

    # More switching keywords
    for i, c1 in enumerate(carriers[:20]):
        for c2 in carriers[:20]:
            if c1 != c2:
                add_keyword(f"transfer number from {c1} to {c2}", "Switching", "Number Transfer", "Transactional", 80)
                add_keyword(f"keep number switch {c1} to {c2}", "Switching", "Number Porting", "Transactional", 80)

    # More support keywords
    device_issues = ['screen crack', 'battery issue', 'speaker problem', 'microphone not working',
                     'camera issue', 'touch screen problem', 'restart loop', 'water damage']
    for issue in device_issues:
        add_keyword(f"phone {issue}", "Support", "Device Issues", "Informational", 40)
        add_keyword(f"fix {issue}", "Support", "Repairs", "Informational", 45)
        add_keyword(f"repair {issue}", "Support", "Repairs", "Commercial", 50)

    # More pricing keywords
    all_prices = ['$10', '$12', '$18', '$22', '$28', '$32', '$38', '$42', '$48', '$52', '$58', '$62', '$68', '$72', '$85', '$95']
    for price in all_prices:
        add_keyword(f"plan for {price}", "Pricing", "Price Plans", "Commercial", 75)
        add_keyword(f"phone plan {price}", "Pricing", "Price Plans", "Commercial", 75)
        add_keyword(f"cheap plan {price}", "Pricing", "Budget Plans", "Commercial", 80)

    # More family plan keywords
    num_lines = ['2', '3', '4', '5', '6', '7', '8']
    for num in num_lines:
        add_keyword(f"{num} line plan", "Family Plans", "Multi-Line", "Commercial", 75)
        add_keyword(f"best {num} line plan", "Family Plans", "Best Multi-Line", "Commercial", 80)
        add_keyword(f"cheap {num} line plan", "Family Plans", "Budget Multi-Line", "Commercial", 80)
        for carrier in carriers[:10]:
            add_keyword(f"{carrier} {num} line plan", "Family Plans", "Carrier Multi-Line", "Commercial", 75)

    # More feature keywords
    streaming = ['netflix', 'hulu', 'disney+', 'hbo max', 'apple tv+', 'amazon prime', 'peacock', 'paramount+']
    for stream in streaming:
        add_keyword(f"plan with {stream}", "Features", "Streaming", "Commercial", 70)
        add_keyword(f"free {stream} phone plan", "Features", "Free Streaming", "Commercial", 75)
        for carrier in carriers[:10]:
            add_keyword(f"{carrier} {stream}", "Features", "Carrier Streaming", "Commercial", 65)
            add_keyword(f"free {stream} {carrier}", "Features", "Carrier Perks", "Commercial", 70)

    # More FAQ keywords
    faq_topics = ['activation', 'porting', 'cancellation', 'contract', 'early termination', 'refund',
                  'warranty', 'insurance', 'autopay', 'paperless billing', 'payment plan']
    for topic in faq_topics:
        add_keyword(f"how to {topic}", "FAQ", "How To", "Informational", 40)
        add_keyword(f"what is {topic}", "FAQ", "Definitions", "Informational", 35)
        for carrier in carriers[:10]:
            add_keyword(f"{carrier} {topic}", "FAQ", "Carrier FAQ", "Informational", 40)

    print(f"\n  Total keywords generated: {keyword_count}")

    # Build taxonomy structure
    print("\nBuilding taxonomy structure...")

    taxonomy = {
        "classification_system": {
            "name": "Telecom Keyword Classification - 10K Sample",
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "total_keywords": keyword_count,
            "description": "10,000 keyword sample dataset for testing telecom classifier"
        },
        "taxonomy": {
            "L1_categories": []
        }
    }

    # Group keywords by category
    category_data = defaultdict(lambda: defaultdict(list))
    for kw, data in keywords.items():
        category_data[data['category']][data['subcategory']].append({
            'keyword': kw,
            'intent': data['intent'],
            'score': data['score']
        })

    # Build L1 categories
    for cat_name, subcats in category_data.items():
        l1 = {
            "id": f"L1_{cat_name.replace(' ', '_').upper()}",
            "name": cat_name,
            "slug": cat_name.lower().replace(' ', '-'),
            "L2_subcategories": []
        }

        for subcat_name, kws in subcats.items():
            l2 = {
                "id": f"L2_{subcat_name.replace(' ', '_').upper()}",
                "name": subcat_name,
                "slug": subcat_name.lower().replace(' ', '-'),
                "L3_intents": [{
                    "id": f"L3_{subcat_name.replace(' ', '_').upper()}_INTENT",
                    "intent_category": kws[0]['intent'] if kws else "Commercial",
                    "intent_subcategory": subcat_name,
                    "commercial_score": kws[0]['score'] if kws else 50,
                    "funnel_stage": "Consideration",
                    "L4_topics": [{
                        "id": f"L4_{subcat_name.replace(' ', '_').upper()}_TOPIC",
                        "topic": subcat_name,
                        "slug": subcat_name.lower().replace(' ', '-'),
                        "L5_keywords": [{"keyword": k['keyword'], "search_volume": 1000, "difficulty": 50} for k in kws]
                    }]
                }]
            }
            l1["L2_subcategories"].append(l2)

        taxonomy["taxonomy"]["L1_categories"].append(l1)

    # Save the dataset
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'telecom-classification-10K.json')

    print(f"\nSaving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(taxonomy, f, indent=2)

    file_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  File size: {file_size:.2f} MB")

    # Print summary
    print("\n" + "=" * 80)
    print("GENERATION SUMMARY")
    print("=" * 80)

    print(f"\n{'Category':<25} {'Target':>10} {'Actual':>10}")
    print("-" * 50)
    for cat, data in categories.items():
        print(f"{cat:<25} {data['target']:>10} {len(data['keywords']):>10}")
    print("-" * 50)
    print(f"{'TOTAL':<25} {sum(c['target'] for c in categories.values()):>10} {keyword_count:>10}")

    print("\n" + "=" * 80)
    print("10K SAMPLE DATASET CREATED SUCCESSFULLY!")
    print("=" * 80)

    return output_path


def test_with_classifier(dataset_path):
    """Test the new dataset with the classifier"""
    from telecom_classifier import TelecomClassifier

    print("\n" + "=" * 80)
    print("TESTING CLASSIFIER WITH 10K DATASET")
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
    ]

    print(f"\nRunning {len(test_queries)} test queries...\n")

    passed = 0
    for query, expected_l1 in test_queries:
        result = classifier.classify_text(query)
        if result:
            actual_l1 = result['classification']['L1']['name']
            is_branded = result['classification']['L2'].get('is_branded', False)
            brand_type = result['classification']['L2'].get('brand_type', '-')

            status = "PASS" if actual_l1 == expected_l1 else "FAIL"
            if actual_l1 == expected_l1:
                passed += 1

            print(f"  [{status}] '{query}'")
            print(f"        Expected: {expected_l1} | Actual: {actual_l1}")
            print(f"        Branded: {is_branded} | Type: {brand_type}")
        else:
            print(f"  [FAIL] '{query}' - No classification")

    print(f"\n  Results: {passed}/{len(test_queries)} passed ({passed/len(test_queries)*100:.0f}%)")

    return passed == len(test_queries)


if __name__ == '__main__':
    dataset_path = generate_10k_sample()
    test_with_classifier(dataset_path)
