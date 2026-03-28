from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
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

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against a user preference profile.

    Returns a tuple of:
      - total score (float, max 5.0)
      - list of human-readable reason strings explaining the score
    """
    score = 0.0
    reasons = []

    # Rule 1 — Genre match: +2.0 pts (strongest categorical signal)
    if song["genre"] == user_prefs.get("genre", ""):
        score += 2.0
        reasons.append(f"genre match: {song['genre']} (+2.0)")

    # Rule 2 — Mood match: +1.0 pt
    if song["mood"] == user_prefs.get("mood", ""):
        score += 1.0
        reasons.append(f"mood match: {song['mood']} (+1.0)")

    # Rule 3 — Energy proximity: up to +1.0 pt
    # Rewards closeness to target — not higher or lower, just nearer
    target_energy = user_prefs.get("energy", 0.5)
    energy_pts = round(1.0 - abs(song["energy"] - target_energy), 3)
    score += energy_pts
    reasons.append(f"energy {song['energy']} vs target {target_energy} (+{energy_pts})")

    # Rule 4 — Acousticness bonus: up to +0.5 pts
    # likes_acoustic=True rewards high acousticness; False rewards low
    likes_acoustic = user_prefs.get("likes_acoustic", False)
    if likes_acoustic:
        acoustic_pts = round(0.5 * song["acousticness"], 3)
    else:
        acoustic_pts = round(0.5 * (1.0 - song["acousticness"]), 3)
    score += acoustic_pts
    reasons.append(f"acousticness {song['acousticness']} (+{acoustic_pts})")

    # Rule 5 — Valence proximity: up to +0.5 pts
    # Default target valence 0.65 (neutral-positive) if not in profile
    target_valence = user_prefs.get("valence", 0.65)
    valence_pts = round(0.5 * (1.0 - abs(song["valence"] - target_valence)), 3)
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
