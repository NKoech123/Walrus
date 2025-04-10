# Superhero Squad Builder

This script builds optimal squads of superheroes based on their powers, leadership abilities, and affinities.

## Tools Used
VS Code with github copilot

## Setup Instructions

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR
.\venv\Scripts\activate  # On Windows
```

2. Install required packages:
```bash
pip install requests
```

## Running the Script

1. Make sure you're in the virtual environment (you should see `(venv)` at the start of your command prompt)

2. Run the script:
```bash
python squads.py
```

## Output

The script will generate a file called `squads_output.json` containing the optimized squads. Each squad entry includes:
- The leader's name
- The squad's score
- Names of all squad members

The squads are sorted by score, with the highest scoring squads appearing first in the file.
