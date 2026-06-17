import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# ── Scoring policy ────────────────────────────────────────────────────────
# All tuning knobs for score_song() live here so the policy is visible and
# adjustable in one place.
GENRE_WEIGHT = 2.0       # categorical: exact genre match
MOOD_WEIGHT = 1.0        # categorical: exact mood match
ENERGY_WEIGHT = 1.0      # proximity: closeness to target energy
ACOUSTIC_WEIGHT = 0.5    # acousticness alignment with likes_acoustic
VALENCE_WEIGHT = 0.5     # proximity: closeness to target valence
DEFAULT_ENERGY = 0.5
DEFAULT_VALENCE = 0.65   # neutral-positive

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # NOT YET IMPLEMENTED — placeholder returns the first k songs unsorted.
        # The real, working scoring/ranking lives in recommend_songs() below.
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # NOT YET IMPLEMENTED — placeholder. Real explanations are built by
        # score_song() below (the human-readable reason strings).
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    int(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs

def _proximity_points(value: float, target: float, weight: float) -> float:
    """
    Reward closeness to a target: full `weight` when value == target,
    decreasing linearly to 0 at a distance of 1.0.
    """
    return round(weight * (1.0 - abs(value - target)), 3)


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against a user preference profile.

    Returns a tuple of:
      - total score (float, max 5.0)
      - list of human-readable reason strings explaining the score
    """
    score = 0.0
    reasons = []

    # Rule 1 — Genre match (strongest categorical signal)
    if song["genre"] == user_prefs.get("genre", ""):
        score += GENRE_WEIGHT
        reasons.append(f"genre match: {song['genre']} (+{GENRE_WEIGHT})")

    # Rule 2 — Mood match
    if song["mood"] == user_prefs.get("mood", ""):
        score += MOOD_WEIGHT
        reasons.append(f"mood match: {song['mood']} (+{MOOD_WEIGHT})")

    # Rule 3 — Energy proximity: rewards closeness to target, not higher/lower
    target_energy = user_prefs.get("energy", DEFAULT_ENERGY)
    energy_pts = _proximity_points(song["energy"], target_energy, ENERGY_WEIGHT)
    score += energy_pts
    reasons.append(f"energy {song['energy']} vs target {target_energy} (+{energy_pts})")

    # Rule 4 — Acousticness bonus
    # likes_acoustic=True rewards high acousticness; False rewards low
    likes_acoustic = user_prefs.get("likes_acoustic", False)
    aligned = song["acousticness"] if likes_acoustic else 1.0 - song["acousticness"]
    acoustic_pts = round(ACOUSTIC_WEIGHT * aligned, 3)
    score += acoustic_pts
    reasons.append(f"acousticness {song['acousticness']} (+{acoustic_pts})")

    # Rule 5 — Valence proximity
    target_valence = user_prefs.get("valence", DEFAULT_VALENCE)
    valence_pts = _proximity_points(song["valence"], target_valence, VALENCE_WEIGHT)
    score += valence_pts
    reasons.append(f"valence {song['valence']} vs target {target_valence} (+{valence_pts})")

    return round(score, 3), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Scores every song in the catalog, ranks them highest-to-lowest,
    and returns the top k results.

    Returns a list of (song_dict, score, explanation) tuples.
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored.append((song, score, explanation))

    # sorted() returns a new list — original `songs` list is not modified
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    return ranked[:k]
