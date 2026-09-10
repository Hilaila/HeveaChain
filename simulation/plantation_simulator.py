"""
HeveaChain V0.1
Simulateur de plantation et cerveau de navigation.

Objectif :
- représenter une plantation réelle ou irrégulière ;
- donner un identifiant à chaque arbre ;
- calculer les distances ;
- choisir automatiquement le prochain arbre à visiter ;
- suivre les arbres déjà traités.

Cette version est une simulation.
Elle ne commande aucun moteur et aucun outil de coupe.
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
    """Carte simplifiée d'une plantation."""

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

        self._generate_plantation()

    def _generate_plantation(self):
        """Génère une plantation avec des positions légèrement irrégulières."""

        tree_id = 1
        y = 0.0

        while y <= self.height:
            x = 0.0

            while x <= self.width:
                # Irrégularité volontaire :
                # les arbres ne sont pas parfaitement alignés.
                offset_x = random.uniform(
                    -self.irregularity,
                    self.irregularity,
                )

                offset_y = random.uniform(
                    -self.irregularity,
                    self.irregularity,
                )

                tree_x = max(0.0, min(self.width, x + offset_x))
                tree_y = max(0.0, min(self.height, y + offset_y))

                self.trees.append(
                    Tree(
                        tree_id=tree_id,
                        x=tree_x,
                        y=tree_y,
                    )
                )

                tree_id += 1
                x += self.tree_spacing

            y += self.row_spacing

    @staticmethod
    def distance(tree_a: Tree, tree_b: Tree) -> float:
        """Calcule la distance entre deux arbres."""

        return hypot(
            tree_a.x - tree_b.x,
            tree_a.y - tree_b.y,
        )

    def nearest_untreated_tree(
        self,
        robot_x: float,
        robot_y: float,
    ):
        """
        Cherche l'arbre non traité le plus proche du robot.
        """

        candidates = [
            tree
            for tree in self.trees
            if not tree.treated
        ]

        if not candidates:
            return None

        return min(
            candidates,
            key=lambda tree: hypot(
                tree.x - robot_x,
                tree.y - robot_y,
            ),
        )

    def mark_treated(self, tree_id: int) -> bool:
        """Marque un arbre comme traité."""

        for tree in self.trees:
            if tree.tree_id == tree_id:
                tree.treated = True
                return True

        return False

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
    """Lance une simulation complète."""

    plantation = HeveaPlantation(
        width=100,
        height=100,
        row_spacing=5,
        tree_spacing=3,
        irregularity=0.50,
        seed=42,
    )

    print("=" * 60)
    print("HEVEACHAIN V0.1")
    print("SIMULATION DE PLANTATION")
    print("=" * 60)

    print("\nPlantation créée.")
    print(f"Nombre total d'arbres : {len(plantation.trees)}")

    print("\nPremiers arbres détectés :")

    for tree in plantation.trees[:10]:
        print(
            f"Arbre {tree.tree_id:03d} "
            f"| X={tree.x:6.2f} m "
            f"| Y={tree.y:6.2f} m"
        )

    # Position initiale du robot.
    robot_x = 0.0
    robot_y = 0.0

    print("\nNavigation du robot :")
    print("-" * 60)

    step = 0

    while True:
        next_tree = plantation.nearest_untreated_tree(
            robot_x,
            robot_y,
        )

        if next_tree is None:
            break

        distance = hypot(
            next_tree.x - robot_x,
            next_tree.y - robot_y,
        )

        step += 1

        print(
            f"Étape {step:03d} | "
            f"Robot → Arbre {next_tree.tree_id:03d} | "
            f"distance = {distance:6.2f} m"
        )

        # Le robot atteint l'arbre.
        robot_x = next_tree.x
        robot_y = next_tree.y

        # Dans cette version, on simule simplement
        # que l'opération sur l'arbre est terminée.
        plantation.mark_treated(next_tree.tree_id)

    stats = plantation.statistics()

    print("\n" + "=" * 60)
    print("FIN DE LA SIMULATION")
    print("=" * 60)

    print(f"Arbres détectés : {stats['total']}")
    print(f"Arbres traités  : {stats['treated']}")
    print(f"Arbres restants : {stats['remaining']}")


if __name__ == "__main__":
    run_simulation()