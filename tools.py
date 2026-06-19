"""
tools.py

The three required FitFindr tools. Each tool is a standalone function that
can be called and tested independently before being wired into the agent loop.

Complete and test each tool before moving to agent.py.

Tools:
    search_listings(description, size, max_price)  -> list[dict]
    suggest_outfit(new_item, wardrobe)              -> str
    create_fit_card(outfit, new_item)               -> str
"""

import os

from dotenv import load_dotenv
from groq import Groq

from utils.data_loader import load_listings

load_dotenv()


# -- Groq client ----------------------------------------------------------------

def _get_groq_client():
    """Initialize and return a Groq client using GROQ_API_KEY from .env."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not set. Add it to a .env file in the project root."
        )
    return Groq(api_key=api_key)


# -- Tool 1: search_listings ----------------------------------------------------

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    listings = load_listings()

    # Filter by price
    if max_price is not None:
        listings = [l for l in listings if l["price"] <= max_price]

    # Filter by size (case-insensitive substring match)
    if size is not None:
        size_lower = size.lower()
        listings = [l for l in listings if size_lower in l["size"].lower()]

    # Score by keyword overlap with description
    keywords = description.lower().split()

    def score(listing):
        searchable = " ".join([
            listing["title"],
            listing["description"],
            listing["category"],
            " ".join(listing["style_tags"]),
            listing.get("brand") or "",
        ]).lower()
        return sum(1 for kw in keywords if kw in searchable)

    # Drop zero-score listings and sort by score descending
    scored = [(listing, score(listing)) for listing in listings]
    scored = [(l, s) for l, s in scored if s > 0]
    scored.sort(key=lambda x: x[1], reverse=True)

    return [l for l, s in scored]


# -- Tool 2: suggest_outfit -----------------------------------------------------

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    client = _get_groq_client()

    item_summary = (
        f"Item: {new_item['title']}\n"
        f"Category: {new_item['category']}\n"
        f"Style tags: {', '.join(new_item['style_tags'])}\n"
        f"Colors: {', '.join(new_item['colors'])}\n"
        f"Condition: {new_item['condition']}\n"
        f"Price: ${new_item['price']}"
    )

    wardrobe_items = wardrobe.get("items", [])

    if not wardrobe_items:
        prompt = (
            f"A user is considering buying this secondhand item:\n\n{item_summary}\n\n"
            "They haven't shared their wardrobe yet. "
            "Suggest 1-2 general outfit ideas: what types of pieces pair well with this item, "
            "what vibe or aesthetic it suits, and one specific styling tip. "
            "Keep it casual and specific — like advice from a friend who knows fashion."
        )
    else:
        wardrobe_text = "\n".join(
            f"- {item['name']} ({item['category']}, {', '.join(item['colors'])})"
            + (f" — {item['notes']}" if item.get("notes") else "")
            for item in wardrobe_items
        )
        prompt = (
            f"A user is considering buying this secondhand item:\n\n{item_summary}\n\n"
            f"Here's what they already own:\n{wardrobe_text}\n\n"
            "Suggest 1-2 complete outfit combinations using the new item and specific pieces "
            "from their wardrobe. Name the exact wardrobe pieces in each suggestion. "
            "Include one styling tip per outfit. "
            "Keep it casual and specific — like advice from a friend who knows fashion."
        )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()


# -- Tool 3: create_fit_card ----------------------------------------------------

def create_fit_card(outfit: str, new_item: dict) -> str:
    if not outfit or not outfit.strip():
        return (
            f"Error: cannot generate a fit card without an outfit suggestion. "
            f"Item was '{new_item.get('title', 'unknown')}' — try running suggest_outfit first."
        )

    client = _get_groq_client()

    prompt = (
        f"Write a 2-4 sentence Instagram/TikTok caption for this thrifted outfit.\n\n"
        f"The thrifted item: {new_item['title']} — ${new_item['price']} from {new_item['platform']}\n"
        f"The full outfit: {outfit}\n\n"
        "Rules:\n"
        "- Sound like a real person posting an OOTD, not a product description\n"
        "- Mention the item name, price, and platform once each, naturally\n"
        "- Be specific about the vibe — name the aesthetic, the feeling, the moment\n"
        "- Keep it short, lowercase, with 1-2 emojis max\n"
        "- Do NOT use hashtags"
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,
    )

    return response.choices[0].message.content.strip()
