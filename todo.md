# 🧾 Assignment 2 — Test Driven Development

### ✅ Project Progress Checklist

---

## 👥 Group Setup

- [x] Group of 2 (max 3) students formed
- [x] Shared Git repository created (GitHub or GitLab) **Hmon**
- [x] Repo initialized with `.gitignore`, `README.md`, `LICENSE.md`, and `requirements.txt` **Hmon**

---

## 🕹️ Game Selection & Design

- [x] Chosen game:
  - [x] Pig (dice game)
  - [ ] War (card game)
- [x] Reviewed official rules (Wikipedia link)
- [x] Decided variation of the game to implement  
       _One-diced Pig_
- [x] Identified main classes (e.g., Game, Player, Deck, Dice, HighScore, Intelligence, etc.)
- [x] Planned object-oriented structure (class diagram draft)
- [x] Defined core gameplay loop using Python’s `cmd` module **Hmon**
- [x] Discuss public methods of our classes

---

## ⚙️ Functional Requirements

- [x] 1-player mode (vs computer) implemented
- [x] 2-player mode implemented
- [x] Player can select and change their name
- [ ] Persistent high-score system (saves across sessions)
- [ ] High scores persist even if player name changes
- [x] Rules of the game viewable
- [x] Full game round playable
- [x] Restart and quit options available
- [x] Cheat function for testing implemented
- [x] Text-based visuals added (ASCII/UTF-8)
- [x] Computer AI implemented
- [ ] Configurable AI difficulty levels---to clarify if dice are rolled one by one or two at once
- [x] Handles invalid input gracefully
- [ ] README includes description of how AI/intelligence works

---

## 🧱 Code Structure & Best Practices

- [x] Each class in its own file
- [x] Object-oriented design used
- [x] Small, clear methods
- [x] Follows **PEP 20 (The Zen of Python)**
- [x] Follows **PEP 8 style guide**
- [x] Functional programming used where appropriate
- [x] > 50 commits and ~10 tags in Git (guideline)
- [x] `Makefile` created (optional but recommended) **Dechen**
  - [x] `make run` – run the game
  - [x] `make test` – run tests
  - [x] `make coverage` – generate coverage report
  - [x] `make lint` – run linters
  - [x] `make doc` – generate documentation
  - [x] `make uml` – generate UML diagrams

---

## 🧪 Unit Testing

- [x] One test file per class
- [x] Each class has at least **10 test cases**
- [x] Each class has at least **20 assertions**
- [ ] Coverage > **90%**
- [ ] Test invalid input cases
- [x] Test AI logic
- [ ] Test persistence (high-score saving/loading)
- [x] README includes instructions to:
  - [x] Run the test suite
  - [x] View coverage report

---

## 📚 Documentation

### 1. Code Documentation

- [x] All classes, methods, and functions have proper **docstrings**

### 2. Auto-generated Documentation

- [ ] Tool chosen (e.g., Sphinx, pdoc, pydoc)
- [ ] HTML documentation generated and stored in `doc/api`
- [ ] Make target `make doc` works
- [ ] README includes instructions to regenerate docs

### 3. UML Diagrams

- [ ] Tool chosen (e.g., pyreverse, )
- [ ] Generated **class diagram** and **package diagram**
- [ ] Stored under `doc/uml`
- [ ] Make target `make uml` works
- [ ] README includes instructions to regenerate UML diagrams

---

## 🧹 Code Style & Linters

- [x] Installed and configured:
  - [x] `pylint`
  - [x] `flake8`
  - [x] `flake8-docstrings`
  - [x] `flake8-polyfill`
- [ ] Lint warnings fixed (not silenced)
- [x] Passes code style check with `black`, `pylint`, and `flake8`
- [x] Add target `make lint`

---

## 📝 README.md (Rebecca)

- [x] Project description
- [x] Game rules and basic info
- [x] Installation instructions
- [x] How to run the game
- [x] How to run tests and view coverage
- [x] How to regenerate documentation
- [x] How to regenerate UML diagrams
- [x] Description of AI/intelligence design
- [x] Project structure overview
- [x] Developer information (optional)

---

## 🎥 Presentation Video

- [ ] 5–7 minute presentation recorded
- [ ] Face visible on camera
- [ ] Introduced yourself and your group
- [ ] Demonstrated the game
- [ ] Explained how it meets requirements
- [ ] Highlighted and explained key code parts
- [ ] Uploaded video (e.g., YouTube – unlisted link)
- [ ] Added video link as comment on Canvas submission

---

## ✅ Self-Test (Before Submission)

- [x] Can install and run from fresh zip/repo
- [x] README complete and clear
- [x] All requirements implemented
- [x] Handles invalid inputs robustly
- [x] Passes code style and linters
- [ ] Test coverage ≥ 90%
- [x] Documentation regenerates correctly
- [x] UML regenerates correctly
- [x] Game functions as expected

---

## 📦 Submission

- [ ] Pack project as `game.zip`
- [ ] Submit to Canvas
- [ ] Include link to repository (optional)
- [ ] Add presentation video link as Canvas comment

---

## 🔍 Opposition (Peer Review)

- [ ] Downloaded assigned projects (2–3)
- [ ] Performed self-test checklist for each
- [ ] Played each game and evaluated quality
- [ ] Reviewed code and structure
- [ ] Wrote feedback summary (1.5–2 pages, PDF):
  - [ ] Game quality
  - [ ] Code/class quality
  - [ ] Suggestions for improvement
- [ ] Submitted PDF review

---
