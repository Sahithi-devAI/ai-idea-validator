"""
Stress test cases across the full idea quality spectrum.
Run manually or integrate into a live evaluation loop.

Each case has:
  idea            — the input
  category        — classification label
  expected_signal — acceptable build signals (evaluator should land in this set)

Usage:
  python tests/stress/ideas.py
"""

STRESS_IDEAS = [
    {
        "category": "great",
        "idea": (
            "A developer tool that automatically identifies and fixes security vulnerabilities "
            "in pull requests before merge, using static analysis and LLM reasoning. "
            "Integrates natively with GitHub and GitLab."
        ),
        "expected_signal": ["strong_yes", "cautious_yes", "explore_more"],
    },
    {
        "category": "incremental",
        "idea": (
            "Another project management app like Trello but with AI-generated task summaries "
            "and priority suggestions."
        ),
        "expected_signal": ["explore_more", "not_recommended"],
    },
    {
        "category": "fake_ai_wrapper",
        "idea": (
            "A customer service chatbot that wraps ChatGPT with a nice UI. "
            "No fine-tuning, no proprietary data, no vertical focus — just a GPT wrapper."
        ),
        "expected_signal": ["not_recommended", "explore_more"],
    },
    {
        "category": "consumer",
        "idea": (
            "An app that helps people decide what to cook based on photos of ingredients "
            "in their fridge, using AI to suggest recipes with what they have."
        ),
        "expected_signal": ["explore_more", "not_recommended"],
    },
    {
        "category": "enterprise",
        "idea": (
            "A compliance automation platform that maps internal policies to regulatory frameworks "
            "(SOC2, GDPR, ISO27001) and auto-generates audit evidence for security reviews."
        ),
        "expected_signal": ["strong_yes", "cautious_yes"],
    },
    {
        "category": "vague",
        "idea": "An AI platform for businesses.",
        "expected_signal": ["explore_more", "not_recommended"],
    },
    {
        "category": "bad",
        "idea": (
            "A social network for pets where owners post photos and AI writes captions. "
            "Monetized through pet product ads."
        ),
        "expected_signal": ["not_recommended", "explore_more"],
    },
    {
        "category": "niche_strong",
        "idea": (
            "A tool for radiologists that uses multimodal AI to flag anomalies in chest X-rays "
            "and generates a structured pre-report, reducing reporting time by 40%."
        ),
        "expected_signal": ["strong_yes", "cautious_yes"],
    },
    {
        "category": "great",
        "idea": (
            "A developer tool that auto-generates realistic synthetic test data directly from "
            "production database schemas, with built-in PII detection and masking. "
            "Integrates with Postgres, MySQL, and Snowflake via CLI or CI pipeline."
        ),
        "expected_signal": ["strong_yes", "cautious_yes"],
    },
    {
        "category": "niche_strong",
        "idea": (
            "An AI platform for independent pharmacists that flags high-risk drug interaction "
            "combinations in real time during prescription dispensing, with dosage adjustment "
            "suggestions for elderly and renal-impaired patients."
        ),
        "expected_signal": ["strong_yes", "cautious_yes"],
    },
    {
        "category": "consumer",
        "idea": (
            "A voice journaling app where users speak freely for 2–5 minutes each day. "
            "AI surfaces recurring emotional patterns over weeks and suggests therapy-style "
            "reflection prompts. No typing, no streaks, no gamification."
        ),
        "expected_signal": ["cautious_yes", "explore_more"],
    },
    {
        "category": "bad",
        "idea": (
            "An NFT marketplace exclusively for AI-generated digital art, with on-chain "
            "royalty tracking and a creator fund paid out in a proprietary token. "
            "Monetized through a 5% transaction fee."
        ),
        "expected_signal": ["not_recommended", "explore_more"],
    },
    {
        "category": "enterprise",
        "idea": (
            "A vendor risk management platform that ingests third-party security questionnaires "
            "(SOC2 reports, SIG lite, CAIQ) and auto-scores supplier risk using AI, replacing "
            "manual analyst review for procurement and InfoSec teams."
        ),
        "expected_signal": ["strong_yes", "cautious_yes"],
    },
]


if __name__ == "__main__":
    import os
    import sys

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

    from dotenv import load_dotenv
    from main import run_evaluation

    load_dotenv()

    provider = os.getenv("LLM_PROVIDER", "anthropic")
    passed = 0
    failed = 0

    for i, case in enumerate(STRESS_IDEAS, 1):
        category = case["category"]
        idea = case["idea"]
        expected = case["expected_signal"]

        print(f"\n[{i}/{len(STRESS_IDEAS)}] {category.upper()}")
        print(f"  Idea: {idea[:80]}{'...' if len(idea) > 80 else ''}")

        try:
            result = run_evaluation(idea, provider=provider)
            signal = result.build_signal.value
            ok = signal in expected
            status = "PASS" if ok else "FAIL"
            if ok:
                passed += 1
            else:
                failed += 1
            print(f"  Signal:   {signal}")
            print(f"  Expected: {expected}")
            print(f"  Result:   {status}")
        except Exception as e:
            failed += 1
            print(f"  ERROR: {e}")

    total = passed + failed
    print(f"\n{'=' * 40}")
    print(f"  {passed}/{total} passed  |  {failed}/{total} failed")
    print(f"{'=' * 40}\n")
