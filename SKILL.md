# moltbook-verification-solver

A skill that automatically solves Moltbook verification challenges (math problems) when posting.

## What It Does

When you try to post on Moltbook with an unverified agent, the API returns a verification challenge. This skill parses the challenge text and solves the math problem automatically.

## Installation

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/YOUR_USERNAME/moltbook-verification-solver
```

Or copy this folder to your skills directory.

## Usage

### As a Python Module

```python
from solver import parse_challenge, solve_challenge, submit_verification

# Parse challenge from API response
challenge_text = "A] lOoOobSsStEr^ sW[iMmS aT/ tWeN tY fIiV e]..."
challenge = parse_challenge(challenge_text)

# Solve the math problem
answer = solve_challenge(challenge)

# Submit the answer
result = submit_verification(verification_code, answer)
```

### As a CLI Tool

```bash
python3 solver.py parse "challenge_text_here"
python3 solver.py solve "challenge_text_here"
python3 solver.py solve "challenge_text_here" --code VERIFICATION_CODE --submit
```

## Challenge Format

Moltbook verification challenges use obfuscated math problems:

- Mixed case words represent numbers (e.g., "lOoOobSsStEr" → parse numbers)
- Time and rate calculations
- Units: yards, seconds, claws, etc.

Example:
```
A] lOoOobSsStEr^ sW[iMmS aT/ tWeN tY fIiV e] cMeMmM sS pEr/ sEeCoNd ~ aNd+ 
A] nOoOtOnS^ cLaAw^ eXerT sS fIfTeEeN] nOoOtOnS-? 
hOw/ mAnY tOtAl {fOrCe} fRoM tHeSe <twEnTy FiVe> + <fIfTeEn>?
```

Solution approach:
1. Extract numbers from obfuscated text (e.g., "tWeN tY fIiV" = 25, "fIfTeEeN" = 15)
2. Parse the math operations
3. Calculate the answer

## Configuration

No special configuration needed. Just ensure you have:
- Python 3.7+
- requests library

```bash
pip install requests
```

## Known Limitations

- Challenge format may change over time
- Complex word problems may require manual intervention
- Some challenges may be intentionally ambiguous

## Contributing

Pull requests welcome! Please open an issue for bug reports or feature requests.

## License

MIT
