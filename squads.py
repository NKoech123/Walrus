import requests
import json
import asyncio
from itertools import combinations


class Hero:
    def __init__(self, name: str, powers: list[str], leadershipAbility: int, affinities: list[str]):
        self.name = name
        self.powers = powers
        self.leadershipAbility = leadershipAbility
        self.affinities = affinities

    def __repr__(self):
        return f"Hero(name={self.name}, leadership={self.leadershipAbility})"


class SquadBuilder:
    def __init__(self, top_n: int = 10):
        self.url = 'https://storage.googleapis.com/dc-recruiting-longform-4d1c78ff/heroes-1460ca6a.json'
        self.top_n = top_n # Number of top superheroes  to consider for each leader

    async def fetch_heroes(self) -> list[Hero]:
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()
            return [Hero(**hero) for hero in data]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            raise e
        
    def is_good_leader(self, hero: Hero) -> bool:
        return hero.leadershipAbility >= 7;

    def calculate_score(self, squad: list[Hero], leader: Hero) -> int:
        """
        Calcualing Score guidelines
            -> 1 POINT for any squad of 4 heroes.
            -> +1 POINT for each unique power possessed by at least one member of the squad.
            -> +MULTIPLIER double the score every time a hero has an affinity for another hero on the
            squad.
            -> +MULTIPLIER double the score if the leader of the squad has a leadershipAbility of 10
        """
      
        score = 1
        powers = set()
        affinity_pairs = 0

        name_map = {hero.name: hero for hero in squad}

        for hero in squad:
            powers.update(hero.powers)
            for ally in hero.affinities:
                if ally in name_map:
                    affinity_pairs += 1

        score += len(powers)
        for _ in range(affinity_pairs):
            score *= 2

        if leader.leadershipAbility == 10:
            score *= 2

        return score
        

    def choose_leader(self, squad: list[Hero]) -> Hero:
        leaders = [h for h in squad if self.is_good_leader(h)]
        if not leaders:
            return None
        
        # Sort by leadershipAbility, then by number of powers, then by lexicographical order of name
        leaders.sort(key=lambda h: (-h.leadershipAbility, -len(h.powers), h.name))

        return leaders[0]
    
    async def build_squad(self):
        heroes = await self.fetch_heroes()
        squads = []
        used_heroes = set()

        leaders = sorted(
            [h for h in heroes if self.is_good_leader(h)],
            key=lambda h: (-h.leadershipAbility, -len(h.powers), -len(h.affinities))
        )

        name_map = {h.name: h for h in heroes}

        while leaders:
            leader = leaders.pop(0)
            if leader.name in used_heroes:
                continue

            # Top candidate pool (affinities first, then power-rich others)
            candidates = [
                h for h in heroes
                if h.name not in used_heroes and h.name != leader.name
            ]

            # Prioritizing affinities
            candidates.sort(
                key=lambda h: (
                    -1 if h.name in leader.affinities else 0,
                    -len(h.powers),
                    h.leadershipAbility
                )
            )

          
            candidates = candidates[:self.top_n]

            best_trio = None
            best_score = -1

            for trio in combinations(candidates, 3):
                squad = [leader, *trio]
                score = self.calculate_score(squad, leader)
                if score > best_score:
                    best_score = score
                    best_trio = trio

            if not best_trio:
                continue

            full_squad = [leader, *best_trio]
            used_heroes.update(h.name for h in full_squad)

            squads.append({
                "leader": leader.name,
                "score": best_score,
                "squad": [h.name for h in full_squad]
            })

        return squads

def main():
    top_n = 30 
    squad_builder = SquadBuilder(top_n=top_n)
    squads = asyncio.run(squad_builder.build_squad())  
    with open("squads_output.json", "w") as f:
        json.dump(squads, f, indent=2)

   

if __name__ == "__main__":
    main()