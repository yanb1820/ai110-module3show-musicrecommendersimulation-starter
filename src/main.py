"""
Command line runner for the Music Recommender Simulation.

Runs six user profiles through the recommender:
  - Three standard profiles (pop, lofi, rock)
  - Three adversarial / edge-case profiles
"""

from recommender import load_songs, recommend_songs


PROFILES = [
    # ── Standard profiles ─────────────────────────────────────────────────
    {
        "name": "High-Energy Pop",
        "prefs": {"genre": "pop", "mood": "happy", "energy": 0.85,
                  "likes_acoustic": False},
    },
    {
        "name": "Chill Lofi",
        "prefs": {"genre": "lofi", "mood": "focused", "energy": 0.38,
                  "likes_acoustic": True},
    },
    {
        "name": "Deep Intense Rock",
        "prefs": {"genre": "rock", "mood": "intense", "energy": 0.92,
                  "likes_acoustic": False},
    },

    # ── Adversarial / edge-case profiles ──────────────────────────────────
    {
        # Conflict: high energy target but sad/melancholy mood
        # Exposes whether energy or mood drives the top result
        "name": "EDGE: High-Energy + Melancholy Mood",
        "prefs": {"genre": "blues", "mood": "melancholy", "energy": 0.95,
                  "likes_acoustic": False},
    },
    {
        # Nonexistent genre and mood — zero categorical matches guaranteed
        # Should expose the energy/valence floor: what is the best score
        # the system can produce with NO category points?
        "name": "EDGE: Unknown Genre + Unknown Mood",
        "prefs": {"genre": "bossa_nova", "mood": "nostalgic_fury", "energy": 0.55,
                  "likes_acoustic": True},
    },
    {
        # Extreme ends: energy target 0.0 and likes_acoustic=True
        # Tests whether very-low-energy ambient songs dominate,
        # or whether acoustic + valence bonuses can surface surprises
        "name": "EDGE: Zero Energy + Max Acoustic",
        "prefs": {"genre": "ambient", "mood": "chill", "energy": 0.0,
                  "likes_acoustic": True},
    },
]


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile in PROFILES:
        name  = profile["name"]
        prefs = profile["prefs"]
        print(f"\n{'='*60}")
        print(f"Profile: {name}")
        print(f"Prefs:   {prefs}")
        print(f"{'='*60}")

        recommendations = recommend_songs(prefs, songs, k=5)

        if not recommendations:
            print("  No recommendations returned.")
            continue

        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n  #{rank}  {song['title']} ({song['genre']} / {song['mood']})")
            print(f"       Score: {score:.3f} / 5.0")
            print(f"       Why:   {explanation}")


if __name__ == "__main__":
    main()
