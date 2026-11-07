"""Aspect and customer-context taxonomy, fixed before labelling.

Derived from the NMF topics and weighted log-odds terms of step 2 (outputs/<source>/topics.json,
logodds.json) and from the beauty review-mining literature; see README.md for the mapping.
The same taxonomy is used for Amazon and Sephora so results are comparable.
"""

ASPECTS = {
    "efficacy": "whether the product does what it is meant to (results, works / doesn't work, visible effect)",
    "skin_reaction": "irritation, breakouts, rash, burning, allergic reaction, or gentle / no reaction",
    "hydration_skin_feel": "moisturising, drying, oily or greasy after-feel, how skin feels after use",
    "texture": "consistency and application feel: thick, thin, runny, sticky, absorbs, spreads, lather",
    "scent": "fragrance or smell of the product",
    "longevity": "how long the effect or wear lasts (stays on, fades, wears off, all day)",
    "colour_shade": "colour, shade match, pigmentation, tone, coverage",
    "hair_result": "hair outcomes: softness, frizz, shine, volume, curls, hold, tangles",
    "packaging": "container, pump, cap, spray nozzle, leaks, broken on arrival, design",
    "size_quantity": "amount, size, how long the supply lasts, smaller than expected",
    "price_value": "price, value for money, expensive, cheap, worth it",
    "authenticity_quality": "fake or counterfeit, expired, old, used, cheap build quality, not as described",
    "delivery_service": "shipping, arrival time, wrong item sent, seller or customer service, returns",
    "ease_of_use": "how easy it is to use or apply; instructions; tools and devices handling",
    "ingredients": "ingredients, natural, chemicals, free-from claims, vegan, cruelty-free",
    "overall": "general verdict with no specific aspect (love it, great, terrible, would buy again)",
}

CONTEXT = {
    "skin_dry": "reviewer says they have dry skin",
    "skin_oily": "oily skin",
    "skin_combination": "combination skin",
    "skin_sensitive": "sensitive or reactive skin",
    "skin_acne": "acne-prone skin or breakouts as a condition",
    "skin_mature": "mature or ageing skin, wrinkles as a concern",
    "hair_fine": "fine or thin hair",
    "hair_thick_coarse": "thick or coarse hair",
    "hair_curly": "curly, wavy or coily hair",
    "hair_damaged": "damaged, colour-treated or dry hair",
    "gift": "bought as a gift for someone else",
    "repeat_buyer": "has bought it before or uses it regularly",
}
