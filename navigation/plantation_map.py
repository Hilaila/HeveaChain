"""
HeveaChain V0.1
Module de cartographie de plantation.
"""

from dataclasses import dataclass
from math import hypot
from typing import List, Tuple


@dataclass
class TreePoint:
    """Position d'un arbre sur la carte."""
    tree_id: int
    x: float
    y: float
    visited: bool = False


class PlantationMap:
    """Carte simplifiée de la plantation."""

    def __init__(self):
        self.trees: List[TreePoint] = []
        self.robot_position: Tuple[float, float] = (0.0, 0.0)
        self.route: List[Tuple[float, float]] = [
            self.robot_position
        ]

    def add_tree(self, tree_id: int, x: float, y: float):
        """Ajoute un arbre à la carte."""
        self.trees.append(
            TreePoint(
                tree_id=tree_id,
                x=x,
                y=y,
            )
        )

    def move_robot(self, x: float, y: float):
        """Déplace virtuellement le robot."""
        self.robot_position = (x, y)
        self.route.append(self.robot_position)

    def distance_to_tree(self, tree: TreePoint) -> float:
        """Calcule la distance entre le robot et un arbre."""
        return hypot(
            self.robot_position[0] - tree.x,
            self.robot_position[1] - tree.y,
        )

    def nearest_unvisited_tree(self):
        """Retourne l'arbre non visité le plus proche."""
        candidates = [
            tree
            for tree in self.trees
            if not tree.visited
        ]

        if not candidates:
            return None

        return min(
            candidates,
            key=self.distance_to_tree,
        )

    def visit_tree(self, tree_id: int) -> bool:
        """Déplace le robot vers un arbre et le marque visité."""
        for tree in self.trees:
            if tree.tree_id == tree_id:
                self.move_robot(tree.x, tree.y)
                tree.visited = True
                return True

        return False

    def map_statistics(self):
        """Retourne les statistiques de la carte."""
        total = len(self.trees)

        visited = sum(
            1
            for tree in self.trees
            if tree.visited
        )

        return {
            "total_trees": total,
            "visited_trees": visited,
            "remaining_trees": total - visited,
            "route_points": len(self.route),
        }

    def display_map(self):
        """Affiche une représentation simple de la carte."""
        print("\n" + "=" * 60)
        print("CARTE HEVEACHAIN")
        print("=" * 60)

        print(
            f"Position robot : "
            f"X={self.robot_position[0]:.2f} m | "
            f"Y={self.robot_position[1]:.2f} m"
        )

        print("\nArbres :")

        for tree in self.trees:
            status = "VISITE" if tree.visited else "NON VISITE"

            print(
                f"Arbre {tree.tree_id:03d} | "
                f"X={tree.x:6.2f} m | "
                f"Y={tree.y:6.2f} m | "
                f"{status}"
            )

        stats = self.map_statistics()

        print("\nStatistiques :")
        print(f"Total arbres    : {stats['total_trees']}")
        print(f"Arbres visités  : {stats['visited_trees']}")
        print(f"Arbres restants : {stats['remaining_trees']}")
        print(f"Points de route : {stats['route_points']}")


def demo():
    """Démonstration du système de cartographie."""

    plantation = PlantationMap()

    plantation.add_tree(1, 0.5, 0.2)
    plantation.add_tree(2, 3.1, 0.1)
    plantation.add_tree(3, 6.0, 0.4)
    plantation.add_tree(4, 0.2, 5.2)
    plantation.add_tree(5, 3.3, 5.0)
    plantation.add_tree(6, 6.2, 5.4)

    plantation.display_map()

    print("\nNavigation automatique :")

    while True:
        next_tree = plantation.nearest_unvisited_tree()

        if next_tree is None:
            break

        distance = plantation.distance_to_tree(next_tree)

        print(
            f"Robot -> Arbre {next_tree.tree_id:03d} "
            f"| distance = {distance:.2f} m"
        )

        plantation.visit_tree(next_tree.tree_id)

    plantation.display_map()


if __name__ == "__main__":
    demo()