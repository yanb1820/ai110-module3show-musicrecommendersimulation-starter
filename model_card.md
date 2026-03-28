# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias

The system ignores tempo preference, lyrics, and listening history, a user who replays a song gets the same result as one who skipped it. Lofi has 3 catalog entries while most genres have only 1, and 11 of 14 mood labels appear on a single song each, making mood nearly useless for most users. The system overfits to energy: high-energy songs like Gym Hero (0.93) surface in almost every high-energy profile regardless of genre, because energy proximity applies to all songs equally. This unintentionally favors users whose genre is overrepresented, a lofi listener gets three genre-matched results while a blues listener gets at most one, through no fault of the scoring logic.

---

## 7. Evaluation

Three profiles were tested: High-Energy Pop, Deep Intense Rock, and an adversarial case with conflicting preferences (high energy + melancholy mood). For the two standard profiles the expected song ranked first — Sunrise City and Storm Runner respectively — which matched musical intuition. A weight-shift experiment (halving genre, doubling energy) was also run to compare how much each rule influenced the rankings. The most surprising result was Gym Hero appearing in the top five for nearly every high-energy profile regardless of genre — it only sees the number 0.93 and considers the job done, like a store clerk handing you workout music whenever you ask for something intense. The adversarial conflicting-preference profile was equally revealing: genre match forced Delta Crossroads to #1 even though its energy (0.48) was far from the target (0.95), showing the system has no way to resolve contradictions in a user's preferences.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
