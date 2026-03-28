# Music Recommender — Data Flow Diagram

Visualize this diagram at [mermaid.live](https://mermaid.live) by pasting the code block below.

```mermaid
flowchart TD
    A([User Preferences\ngenre · mood · energy\nlikes_acoustic]) --> D

    B[("songs.csv\n18 songs")] --> C[load_songs\nparse CSV rows\ninto Song objects]
    C --> D

    D[[recommend\nsongs, user, k]] --> E

    E --> F{More songs\nto score?}

    F -- Yes --> G[Take next Song]
    G --> H1[genre match?\n+2.0 pts]
    H1 --> H2[mood match?\n+1.0 pts]
    H2 --> H3[energy proximity\n1.0 - abs diff]
    H3 --> H4[acousticness bonus\n±0.5 pts]
    H4 --> H5[valence proximity\n±0.5 pts]
    H5 --> H6[sum all points\nmax = 5.0]
    H6 --> H7[("scored_list\n[(song, score)]")]
    H7 --> F

    F -- No --> I[sort scored_list\nby score DESC]
    I --> J[slice top K]
    J --> K[("Output\n[(song, score, explanation)]\nranked #1 → #K")]
```

## Data Flow Summary

| Stage | What happens |
|---|---|
| **Input** | User preferences + songs.csv loaded into Song objects |
| **Process** | Every song scored against 5 rules (max 5.0 pts each) |
| **Output** | Sorted list sliced to top-K recommendations |

## Scoring Rules

| Rule | Max Points |
|---|---|
| Genre match | +2.0 |
| Mood match | +1.0 |
| Energy proximity `1.0 - abs(song.energy - target)` | +1.0 |
| Acousticness bonus `0.5 * acousticness (or inverse)` | +0.5 |
| Valence proximity `0.5 * (1.0 - abs(song.valence - 0.65))` | +0.5 |
| **Total** | **5.0** |
