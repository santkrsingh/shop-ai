"""
Multi-Agent Shopping System
Agents: QueryUnderstanding, ProductSearch, ReviewAnalysis, PriceIntelligence, Recommendation, Orchestrator
Uses rule-based NLP + ML for a working prototype without requiring external LLM API.
"""
import re
import math
import statistics
from typing import Optional
from datetime import datetime, timedelta


# ─────────────────────────────────────────────
# AGENT 1: Query Understanding Agent
# ─────────────────────────────────────────────

class QueryUnderstandingAgent:
    """Parse natural language queries into structured search parameters."""
    
    CATEGORY_KEYWORDS = {
        "Laptops": ["laptop", "notebook", "ultrabook", "macbook", "chromebook", "gaming laptop"],
        "Smartphones": ["phone", "smartphone", "mobile", "iphone", "android", "5g phone"],
        "Headphones": ["headphone", "earphone", "earbud", "airpods", "headset", "earbuds", "wireless headphone"],
        "TVs": ["tv", "television", "smart tv", "oled tv", "qled", "monitor"],
        "Tablets": ["tablet", "ipad", "tab", "kindle"],
        "Cameras": ["camera", "dslr", "mirrorless", "webcam", "action camera"],
    }

    USE_CASE_KEYWORDS = {
        "gaming": ["gaming", "game", "fps", "gpu", "graphics card", "rtx", "gtx", "bgmi", "pubg", "valorant"],
        "student": ["student", "college", "cse", "engineering", "university", "study", "coding", "programming"],
        "professional": ["work", "office", "professional", "business", "excel", "presentation", "remote work"],
        "creator": ["content creator", "youtube", "video editing", "photography", "design", "graphic"],
        "travel": ["travel", "portable", "lightweight", "battery life", "thin"],
    }

    SPEC_PATTERNS = {
        "ram": r"(\d+)\s*gb\s*ram|(\d+)\s*gb\s*memory",
        "storage": r"(\d+)\s*(?:gb|tb)\s*(?:ssd|hdd|storage|nvme)",
        "budget_max": r"under\s*[₹rs]?\s*(\d+[\d,]*)|below\s*[₹rs]?\s*(\d+[\d,]*)|max.*?[₹rs]?\s*(\d+[\d,]*)|budget.*?[₹rs]?\s*(\d+[\d,]*)|less than\s*[₹rs]?\s*(\d+[\d,]*)",
        "budget_min": r"above\s*[₹rs]?\s*(\d+[\d,]*)|more than\s*[₹rs]?\s*(\d+[\d,]*)|atleast\s*[₹rs]?\s*(\d+[\d,]*)",
        "display": r"(\d+)\s*(?:inch|\")\s*(?:display|screen)",
        "battery": r"(\d+)\s*(?:hour|hr).*?battery",
    }

    BRAND_LIST = [
        "asus", "lenovo", "hp", "dell", "apple", "acer", "msi", "samsung",
        "oneplus", "xiaomi", "redmi", "realme", "vivo", "oppo", "sony",
        "bose", "jbl", "sennheiser", "lg", "mi"
    ]

    GPU_KEYWORDS = {
        "dedicated_gpu": ["dedicated gpu", "discrete gpu", "rtx", "gtx", "rx 580", "radeon", "nvidia", "amd gpu", "gpu"],
        "integrated_gpu": ["integrated", "integrated graphics"]
    }

    def parse(self, query: str) -> dict:
        q = query.lower().strip()

        result = {
            "original_query": query,
            "category": self._extract_category(q),
            "budget_max": self._extract_budget_max(q),
            "budget_min": self._extract_budget_min(q),
            "brands": self._extract_brands(q),
            "use_cases": self._extract_use_cases(q),
            "specs": self._extract_specs(q),
            "sort_by": self._extract_sort(q),
            "intent": self._classify_intent(q),
        }

        return result

    def _extract_category(self, q: str) -> Optional[str]:
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in q:
                    return category
        return None

    def _extract_budget_max(self, q: str) -> Optional[float]:
        pattern = self.SPEC_PATTERNS["budget_max"]
        match = re.search(pattern, q, re.IGNORECASE)
        if match:
            val = next(v for v in match.groups() if v is not None)
            return float(val.replace(",", ""))
        # Handle "70000" or "70k"
        k_match = re.search(r"(\d+)\s*k\b", q)
        if k_match:
            return float(k_match.group(1)) * 1000
        return None

    def _extract_budget_min(self, q: str) -> Optional[float]:
        pattern = self.SPEC_PATTERNS["budget_min"]
        match = re.search(pattern, q, re.IGNORECASE)
        if match:
            val = next(v for v in match.groups() if v is not None)
            return float(val.replace(",", ""))
        return None

    def _extract_brands(self, q: str) -> list:
        return [b.capitalize() for b in self.BRAND_LIST if b in q]

    def _extract_use_cases(self, q: str) -> list:
        cases = []
        for use_case, keywords in self.USE_CASE_KEYWORDS.items():
            if any(kw in q for kw in keywords):
                cases.append(use_case)
        return cases

    def _extract_specs(self, q: str) -> dict:
        specs = {}
        
        ram_match = re.search(self.SPEC_PATTERNS["ram"], q)
        if ram_match:
            val = next(v for v in ram_match.groups() if v is not None)
            specs["min_ram_gb"] = int(val)
        
        # GPU requirement
        for spec_key, keywords in self.GPU_KEYWORDS.items():
            if any(kw in q for kw in keywords):
                specs["gpu_type"] = spec_key
                break
        
        # SSD requirement
        if "ssd" in q or "nvme" in q:
            specs["storage_type"] = "SSD"
        
        return specs

    def _extract_sort(self, q: str) -> str:
        if any(w in q for w in ["best", "top", "recommend", "suggest"]):
            return "recommendation_score"
        if any(w in q for w in ["cheap", "affordable", "budget", "lowest price"]):
            return "price_asc"
        if any(w in q for w in ["premium", "best quality", "highest rated"]):
            return "rating_desc"
        return "recommendation_score"

    def _classify_intent(self, q: str) -> str:
        if any(w in q for w in ["compare", "vs", "versus", "difference"]):
            return "compare"
        if any(w in q for w in ["price", "cost", "how much", "cheap"]):
            return "price_check"
        return "product_search"


# ─────────────────────────────────────────────
# AGENT 2: Review Analysis Agent
# ─────────────────────────────────────────────

class ReviewAnalysisAgent:
    """Analyze product reviews using rule-based sentiment analysis."""

    POSITIVE_WORDS = {
        "excellent", "amazing", "fantastic", "great", "good", "best", "perfect",
        "outstanding", "superb", "brilliant", "awesome", "love", "incredible",
        "impressive", "wonderful", "exceptional", "satisfied", "happy", "recommend",
        "worth", "fast", "smooth", "beautiful", "premium", "solid", "reliable",
        "stunning", "gorgeous", "clean", "efficient", "powerful", "snappy"
    }

    NEGATIVE_WORDS = {
        "bad", "poor", "terrible", "awful", "horrible", "disappointing", "worst",
        "slow", "laggy", "cheap", "fragile", "broken", "issue", "problem",
        "complaint", "defective", "loud", "noisy", "hot", "overheating", "bulky",
        "heavy", "expensive", "pricey", "bloatware", "annoying", "frustrating",
        "average", "mediocre", "weak", "dim", "bleed", "rattle"
    }

    ASPECT_KEYWORDS = {
        "performance": ["performance", "speed", "fast", "slow", "lag", "processor", "cpu", "gpu", "ram"],
        "battery": ["battery", "charging", "power", "hours", "drain", "charge"],
        "display": ["display", "screen", "monitor", "brightness", "color", "resolution", "oled", "amoled"],
        "build_quality": ["build", "quality", "material", "premium", "plastic", "metal", "aluminum", "weight"],
        "camera": ["camera", "photo", "picture", "video", "megapixel", "autofocus", "zoom"],
        "value": ["value", "worth", "price", "money", "budget", "expensive", "affordable"],
        "software": ["software", "ui", "os", "android", "ios", "bloatware", "update", "feature"],
        "sound": ["sound", "audio", "bass", "treble", "noise cancellation", "anc", "microphone"],
    }

    def analyze(self, reviews: list) -> dict:
        if not reviews:
            return self._empty_analysis()

        sentiments = []
        aspect_scores = {a: {"pos": 0, "neg": 0, "mentions": 0} for a in self.ASPECT_KEYWORDS}
        pros_raw = []
        cons_raw = []
        all_words = []

        for review in reviews:
            text = (review.get("body", "") + " " + review.get("title", "")).lower()
            words = re.findall(r'\b\w+\b', text)
            all_words.extend(words)

            pos_count = sum(1 for w in words if w in self.POSITIVE_WORDS)
            neg_count = sum(1 for w in words if w in self.NEGATIVE_WORDS)
            
            rating = review.get("rating", 3.0)
            sentiment_score = (pos_count - neg_count) + (rating - 3) * 2
            sentiments.append(sentiment_score)

            # Aspect analysis
            for aspect, keywords in self.ASPECT_KEYWORDS.items():
                for kw in keywords:
                    if kw in text:
                        aspect_scores[aspect]["mentions"] += 1
                        # Check surrounding context for sentiment
                        idx = text.find(kw)
                        context = text[max(0, idx-30):idx+50]
                        ctx_words = re.findall(r'\b\w+\b', context)
                        if any(w in self.POSITIVE_WORDS for w in ctx_words):
                            aspect_scores[aspect]["pos"] += 1
                        if any(w in self.NEGATIVE_WORDS for w in ctx_words):
                            aspect_scores[aspect]["neg"] += 1
                        break

            # Extract sentence-level pros/cons
            sentences = re.split(r'[.!?]', text)
            for sent in sentences:
                sent_words = re.findall(r'\b\w+\b', sent)
                has_pos = any(w in self.POSITIVE_WORDS for w in sent_words)
                has_neg = any(w in self.NEGATIVE_WORDS for w in sent_words)
                if has_pos and not has_neg and len(sent.strip()) > 20:
                    pros_raw.append(sent.strip().capitalize())
                elif has_neg and not has_pos and len(sent.strip()) > 20:
                    cons_raw.append(sent.strip().capitalize())

        # Overall sentiment
        avg_sentiment = statistics.mean(sentiments) if sentiments else 0
        avg_rating = statistics.mean([r.get("rating", 3) for r in reviews])

        # Top aspects
        aspect_summaries = []
        for aspect, data in aspect_scores.items():
            if data["mentions"] > 0:
                score = data["pos"] - data["neg"]
                aspect_summaries.append({
                    "aspect": aspect.replace("_", " ").title(),
                    "score": score,
                    "sentiment": "positive" if score > 0 else ("negative" if score < 0 else "neutral"),
                    "mentions": data["mentions"]
                })
        aspect_summaries.sort(key=lambda x: x["mentions"], reverse=True)

        # Deduplicate pros/cons
        pros = list(dict.fromkeys(pros_raw))[:5]
        cons = list(dict.fromkeys(cons_raw))[:4]

        # Generate AI summary
        summary = self._generate_summary(reviews, avg_rating, pros, cons, aspect_summaries)

        return {
            "total_reviews": len(reviews),
            "average_rating": round(avg_rating, 2),
            "sentiment_score": round(avg_sentiment, 2),
            "overall_sentiment": "positive" if avg_sentiment > 1 else ("negative" if avg_sentiment < -1 else "neutral"),
            "rating_distribution": self._rating_distribution(reviews),
            "aspect_analysis": aspect_summaries[:6],
            "pros": pros,
            "cons": cons,
            "summary": summary,
        }

    def _rating_distribution(self, reviews: list) -> dict:
        dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for r in reviews:
            rating = round(r.get("rating", 3))
            dist[min(5, max(1, rating))] += 1
        return dist

    def _generate_summary(self, reviews, avg_rating, pros, cons, aspects):
        count = len(reviews)
        sentiment_word = "highly positive" if avg_rating >= 4.3 else ("positive" if avg_rating >= 3.8 else ("mixed" if avg_rating >= 3.0 else "mostly negative"))
        
        top_pros = [p[:60] for p in pros[:2]]
        top_cons = [c[:60] for c in cons[:1]]

        summary = f"Based on {count} reviews (avg: {avg_rating:.1f}★), customer sentiment is {sentiment_word}. "
        
        if top_pros:
            summary += f"Customers particularly appreciate: {'; '.join(top_pros).rstrip('.').lower()}. "
        
        top_aspects = [a for a in aspects if a["sentiment"] == "positive"][:2]
        if top_aspects:
            summary += f"Stand-out strengths include {' and '.join(a['aspect'].lower() for a in top_aspects)}. "
        
        if top_cons:
            summary += f"Notable concerns: {top_cons[0].rstrip('.').lower()}."

        return summary

    def _empty_analysis(self):
        return {
            "total_reviews": 0, "average_rating": 0, "sentiment_score": 0,
            "overall_sentiment": "no_reviews", "rating_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            "aspect_analysis": [], "pros": [], "cons": [], "summary": "No reviews available."
        }


# ─────────────────────────────────────────────
# AGENT 3: Price Intelligence Agent
# ─────────────────────────────────────────────

class PriceIntelligenceAgent:
    """Analyze price history and predict price trends."""

    def analyze(self, product_id: int, listings: list, price_history: list) -> dict:
        if not listings:
            return {}

        prices = [l["price"] for l in listings if l.get("price")]
        best_price = min(prices)
        best_listing = min(listings, key=lambda x: x.get("price", float("inf")))

        history_prices = [h["price"] for h in price_history]
        
        if history_prices:
            avg_price = statistics.mean(history_prices)
            min_price_ever = min(history_prices)
            max_price_ever = max(history_prices)
        else:
            avg_price = best_price
            min_price_ever = best_price
            max_price_ever = best_price

        # Price trend (simple linear regression on recent history)
        trend = self._calculate_trend(price_history)
        
        # Price prediction (30 days out)
        predicted_price = self._predict_price(best_price, trend)
        
        # Deal score (0-100)
        deal_score = self._calculate_deal_score(best_price, avg_price, min_price_ever, max_price_ever)
        
        # Recommendation
        recommendation = self._buy_recommendation(deal_score, trend)

        return {
            "current_best_price": best_price,
            "best_platform": best_listing.get("platform"),
            "average_historical_price": round(avg_price),
            "lowest_price_ever": round(min_price_ever),
            "highest_price_ever": round(max_price_ever),
            "price_trend": trend,
            "predicted_price_30d": round(predicted_price),
            "deal_score": deal_score,
            "buy_recommendation": recommendation,
            "savings_vs_avg": round(avg_price - best_price),
            "savings_vs_highest": round(max_price_ever - best_price),
            "price_drop_from_highest": round((max_price_ever - best_price) / max_price_ever * 100, 1),
        }

    def _calculate_trend(self, history: list) -> str:
        if len(history) < 3:
            return "stable"
        
        prices = [h["price"] for h in sorted(history, key=lambda x: x.get("date", ""))]
        
        # Compare first third vs last third
        n = len(prices)
        early_avg = statistics.mean(prices[:n//3]) if n >= 3 else prices[0]
        late_avg = statistics.mean(prices[-(n//3):]) if n >= 3 else prices[-1]
        
        change_pct = (late_avg - early_avg) / early_avg * 100
        
        if change_pct < -5:
            return "falling"
        elif change_pct < -2:
            return "slightly_falling"
        elif change_pct > 5:
            return "rising"
        elif change_pct > 2:
            return "slightly_rising"
        else:
            return "stable"

    def _predict_price(self, current_price: float, trend: str) -> float:
        trend_factors = {
            "falling": 0.94,
            "slightly_falling": 0.97,
            "stable": 0.99,
            "slightly_rising": 1.02,
            "rising": 1.05,
        }
        factor = trend_factors.get(trend, 0.99)
        return current_price * factor

    def _calculate_deal_score(self, current: float, avg: float, min_p: float, max_p: float) -> int:
        if max_p == min_p:
            return 50
        
        # Score based on position in historical range (100 = at all-time low, 0 = at all-time high)
        position_score = max(0, min(100, int((max_p - current) / (max_p - min_p) * 100)))
        
        # Bonus for being below average
        vs_avg_bonus = max(0, min(20, int((avg - current) / avg * 100)))
        
        deal_score = min(100, position_score + vs_avg_bonus // 2)
        return deal_score

    def _buy_recommendation(self, deal_score: int, trend: str) -> str:
        if deal_score >= 75:
            return "🟢 Excellent time to buy — price is near historical low!"
        elif deal_score >= 55 and trend in ("falling", "slightly_falling"):
            return "🟡 Good deal — price trending down, could drop more but current price is fair."
        elif deal_score >= 50:
            return "🟡 Fair deal — price is average. Acceptable if you need it now."
        elif trend in ("falling", "slightly_falling"):
            return "⏳ Wait — price is actively falling. Better deal expected soon."
        else:
            return "🔴 Price is above average. Consider waiting for a sale."


# ─────────────────────────────────────────────
# AGENT 4: Recommendation Agent
# ─────────────────────────────────────────────

class RecommendationAgent:
    """Score and rank products based on user requirements."""

    def score(self, product: dict, parsed_query: dict) -> dict:
        score = 0.0
        explanations = []

        budget_max = parsed_query.get("budget_max")
        budget_min = parsed_query.get("budget_min")
        use_cases = parsed_query.get("use_cases", [])
        req_specs = parsed_query.get("specs", {})
        brands = parsed_query.get("brands", [])

        best_price = product.get("best_price", 0)
        specs = product.get("specifications", {})
        avg_rating = product.get("avg_rating", 3.0)

        # ── Budget fit (0-25 pts) ──
        if budget_max and best_price > 0:
            if best_price <= budget_max:
                budget_margin = (budget_max - best_price) / budget_max
                budget_pts = 15 + min(10, int(budget_margin * 30))
                score += budget_pts
                explanations.append(f"✅ Within budget (₹{best_price:,.0f} ≤ ₹{budget_max:,.0f})")
            else:
                over_pct = (best_price - budget_max) / budget_max * 100
                score -= min(30, over_pct * 2)
                explanations.append(f"❌ Over budget by {over_pct:.0f}%")

        # ── Rating score (0-20 pts) ──
        rating_pts = (avg_rating - 1) / 4 * 20
        score += rating_pts
        if avg_rating >= 4.3:
            explanations.append(f"⭐ Highly rated ({avg_rating:.1f}/5)")

        # ── Spec matching (0-25 pts) ──
        spec_text = " ".join(str(v).lower() for v in specs.values())
        
        if req_specs.get("min_ram_gb"):
            ram_gb = req_specs["min_ram_gb"]
            ram_match = re.search(r"(\d+)\s*gb", spec_text)
            if ram_match:
                found_ram = int(ram_match.group(1))
                if found_ram >= ram_gb:
                    score += 12
                    explanations.append(f"✅ Has {found_ram}GB RAM (required: {ram_gb}GB)")
                else:
                    score -= 10
                    explanations.append(f"❌ Only {found_ram}GB RAM (required: {ram_gb}GB)")

        if req_specs.get("gpu_type") == "dedicated_gpu":
            if any(g in spec_text for g in ["rtx", "gtx", "radeon", "nvidia", "4060", "4070", "4080"]):
                score += 13
                explanations.append("✅ Has dedicated GPU")
            else:
                score -= 15
                explanations.append("❌ No dedicated GPU found")

        if req_specs.get("storage_type") == "SSD":
            if "ssd" in spec_text or "nvme" in spec_text:
                score += 8
                explanations.append("✅ Has SSD storage")

        # ── Use case match (0-15 pts) ──
        product_desc = (product.get("description", "") + " " + product.get("subcategory", "")).lower()
        
        use_case_pts = 0
        for use_case in use_cases:
            if use_case == "gaming" and any(w in product_desc for w in ["gaming", "game", "rtx", "gtx"]):
                use_case_pts += 8
                explanations.append("🎮 Optimized for gaming")
            elif use_case == "student" and any(w in product_desc for w in ["student", "ultrabook", "portable", "slim"]):
                use_case_pts += 6
                explanations.append("🎓 Good for students")
            elif use_case == "professional" and any(w in product_desc for w in ["professional", "business", "pro"]):
                use_case_pts += 5
        score += min(15, use_case_pts)

        # ── Brand preference (5 pts) ──
        if brands and product.get("brand", "") in brands:
            score += 5
            explanations.append(f"✅ Preferred brand: {product['brand']}")

        # ── Deal score bonus (0-10 pts) ──
        deal_score = product.get("deal_score", 50)
        deal_pts = deal_score / 10
        score += deal_pts
        if deal_score >= 70:
            explanations.append(f"🔥 Great deal (score: {deal_score}/100)")

        # ── Value ratio (0-5 pts) ──
        value_ratio = avg_rating / (best_price / 10000) if best_price > 0 else 0
        score += min(5, value_ratio * 0.5)

        final_score = max(0, min(100, score))

        return {
            "recommendation_score": round(final_score, 1),
            "explanations": explanations,
            "verdict": self._get_verdict(final_score),
        }

    def _get_verdict(self, score: float) -> str:
        if score >= 80:
            return "🏆 Top Pick"
        elif score >= 65:
            return "👍 Highly Recommended"
        elif score >= 50:
            return "✔️ Good Choice"
        elif score >= 35:
            return "⚠️ Consider Alternatives"
        else:
            return "❌ Not Recommended"


# ─────────────────────────────────────────────
# ORCHESTRATOR
# ─────────────────────────────────────────────

class ShoppingOrchestrator:
    """Coordinates all agents to process a shopping query end-to-end."""

    def __init__(self):
        self.query_agent = QueryUnderstandingAgent()
        self.review_agent = ReviewAnalysisAgent()
        self.price_agent = PriceIntelligenceAgent()
        self.recommendation_agent = RecommendationAgent()

    def process_query(self, query: str, products_with_data: list) -> dict:
        """
        Full pipeline: query → parse → score products → return ranked results with explanations.
        """
        # Step 1: Parse query
        parsed = self.query_agent.parse(query)

        # Step 2: Score each product
        scored_products = []
        for product in products_with_data:
            score_data = self.recommendation_agent.score(product, parsed)
            scored_product = {**product, **score_data}
            scored_products.append(scored_product)

        # Step 3: Sort by score
        scored_products.sort(key=lambda x: x["recommendation_score"], reverse=True)

        # Step 4: Generate response narrative
        narrative = self._generate_narrative(query, parsed, scored_products[:3])

        return {
            "query": query,
            "parsed_query": parsed,
            "results": scored_products,
            "top_picks": scored_products[:3],
            "narrative": narrative,
            "total_found": len(scored_products),
        }

    def _generate_narrative(self, query: str, parsed: dict, top_products: list) -> str:
        if not top_products:
            return "No products found matching your requirements. Try adjusting your budget or specifications."

        parts = []
        parts.append(f"I found {len(top_products)} great options for your query.")

        if parsed.get("category"):
            parts.append(f"Searching in **{parsed['category']}**.")

        if parsed.get("budget_max"):
            parts.append(f"Budget cap: ₹{parsed['budget_max']:,.0f}.")

        if parsed.get("specs", {}).get("min_ram_gb"):
            parts.append(f"Minimum {parsed['specs']['min_ram_gb']}GB RAM required.")

        if parsed.get("specs", {}).get("gpu_type") == "dedicated_gpu":
            parts.append("Dedicated GPU required.")

        best = top_products[0]
        parts.append(
            f"\n\n**🏆 Top Pick: {best['name']}** (Score: {best['recommendation_score']}/100) "
            f"at ₹{best['best_price']:,.0f} from {best.get('best_platform', 'N/A')}. "
            f"{best.get('verdict', '')}"
        )

        if len(top_products) > 1:
            runner = top_products[1]
            parts.append(
                f"\n**Runner-up: {runner['name']}** at ₹{runner['best_price']:,.0f} — Score: {runner['recommendation_score']}/100."
            )

        return " ".join(parts)
