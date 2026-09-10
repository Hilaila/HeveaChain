"""
HeveaChain V0.1
Simulateur de plantation irrégulière.

Ce module simule une plantation réelle :
- arbres espacés de manière irrégulière
- identification individuelle des arbres
- position du robot
- recherche de l'arbre non traité le plus proche
- suivi des arbres traités
"""

from dataclasses import dataclass
from math import hypot
import random


@dataclass
class Tree:
    """Représente un arbre dans la plantation."""
    tree_id: int
    x: float
    y: float
    treated: bool = False


class HeveaPlantation:
    """Simulateur d'une plantation d'hévéas."""

    def __init__(
        self,
        width: float,
        height: float,
        row_spacing: float,
        tree_spacing: float,
        irregularity: float = 0.50,
        seed: int = 42,
    ):
        self.width = width
        self.height = height
        self.row_spacing = row_spacing
        self.tree_spacing = tree_spacing
        self.irregularity = irregularity

        random.seed(seed)

        self.trees = []
        self.robot_x = 0.0
        self.robot_y = 0.0

        self._generate_plantation()

    def _generate_plantation(self):
        """Génère une plantation avec des positions légèrement irrégulières."""

        tree_id = 1
        y = 0.0

        while y <= self.height:
            x = 0.0

            while x <= self.width:
                random_x = x + random.uniform(
                    -self.irregularity,
                    self.irregularity,
                )

                random_y = y + random.uniform(
                    -self.irregularity,
                    self.irregularity,
                )

                random_x = max(0.0, min(self.width, random_x))
                random_y = max(0.0, min(self.height, random_y))

                self.trees.append(
                    Tree(
                        tree_id=tree_id,
                        x=random_x,
                        y=random_y,
                    )
                )

                tree_id += 1
                x += self.tree_spacing

            y += self.row_spacing

    def distance_to_tree(self, tree: Tree) -> float:
        """Calcule la distance entre le robot et un arbre."""

        return hypot(
            self.robot_x - tree.x,
            self.robot_y - tree.y,
        )

    def nearest_untreated_tree(self):
        """Recherche l'arbre non traité le plus proche."""

        untreated = [
            tree
            for tree in self.trees
            if not tree.treated
        ]

        if not untreated:
            return None

        return min(
            untreated,
            key=self.distance_to_tree,
        )

    def move_to_tree(self, tree: Tree):
        """Déplace virtuellement le robot jusqu'à l'arbre."""

        self.robot_x = tree.x
        self.robot_y = tree.y

    def treat_tree(self, tree: Tree):
        """Marque un arbre comme traité."""

        tree.treated = True

    def statistics(self):
        """Retourne les statistiques de la plantation."""

        total = len(self.trees)

        treated = sum(
            1
            for tree in self.trees
            if tree.treated
        )

        remaining = total - treated

        return {
            "total": total,
            "treated": treated,
            "remaining": remaining,
        }


def run_simulation():
    """Lance une simulation HeveaChain V0.1."""

    plantation = HeveaPlantation(
        width=100.0,
        height=100.0,
        row_spacing=5.0,
        tree_spacing=3.0,
        irregularity=0.50,
        seed=42,
    )

    print("=" * 60)
    print("HEVEACHAIN V0.1")
    print("SIMULATION DE PLANTATION")
    print("=" * 60)

    stats = plantation.statistics()

    print(f"\nSurface : {plantation.width} m x {plantation.height} m")
    print(f"Nombre d'arbres : {stats['total']}")

    print("\nPremiers arbres détectés :")

    for tree in plantation.trees[:10]:
        print(
            f"Arbre {tree.tree_id:03d} "
            f"| X={tree.x:6.2f} m "
            f"| Y={tree.y:6.2f} m"
        )

    print("\nNavigation autonome simulée :")

    steps = 0

    while True:
        next_tree = plantation.nearest_untreated_tree()

        if next_tree is None:
            break

        distance = plantation.distance_to_tree(next_tree)

        plantation.move_to_tree(next_tree)
        plantation.treat_tree(next_tree)

        steps += 1

        if steps <= 10:
            print(
                f"Robot -> Arbre {next_tree.tree_id:03d} "
                f"| distance = {distance:.2f} m "
                f"| traité"
            )

    stats = plantation.statistics()

    print("\n" + "=" * 60)
    print("FIN DE LA SIMULATION")
    print("=" * 60)

    print(f"Total arbres    : {stats['total']}")
    print(f"Arbres traités  : {stats['treated']}")
    print(f"Arbres restants : {stats['remaining']}")
    print(f"Déplacements    : {steps}")
    print(
        f"Position finale : "
        f"X={plantation.robot_x:.2f} m "
        f"| Y={plantation.robot_y:.2f} m"
    )


if __name__ == "__main__":
    run_simulation()