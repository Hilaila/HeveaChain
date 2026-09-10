"""
HeveaChain V0.2
Carte graphique d'une plantation irrégulière.

Affiche :
- les arbres de la plantation ;
- les arbres déjà traités ;
- la position du robot ;
- le parcours autonome du robot.
"""

import matplotlib.pyplot as plt

from plantation_simulator import HeveaPlantation


def run_visual_simulation():
    """Affiche la plantation et le parcours du robot."""

    plantation = HeveaPlantation(
        width=100.0,
        height=100.0,
        row_spacing=5.0,
        tree_spacing=3.0,
        irregularity=0.50,
        seed=42,
    )

    route_x = [plantation.robot_x]
    route_y = [plantation.robot_y]

    while True:
        next_tree = plantation.nearest_untreated_tree()

        if next_tree is None:
            break

        plantation.move_to_tree(next_tree)
        plantation.treat_tree(next_tree)

        route_x.append(plantation.robot_x)
        route_y.append(plantation.robot_y)

    tree_x = [tree.x for tree in plantation.trees]
    tree_y = [tree.y for tree in plantation.trees]

    plt.figure(figsize=(10, 10))

    plt.scatter(
        tree_x,
        tree_y,
        s=18,
        label="Arbres"
    )

    plt.plot(
        route_x,
        route_y,
        linewidth=1,
        label="Parcours HeveaChain"
    )

    plt.scatter(
        [route_x[0]],
        [route_y[0]],
        s=100,
        marker="s",
        label="Départ"
    )

    plt.scatter(
        [route_x[-1]],
        [route_y[-1]],
        s=100,
        marker="X",
        label="Position finale"
    )

    plt.title("HeveaChain V0.2 — Carte de plantation")
    plt.xlabel("Position X (m)")
    plt.ylabel("Position Y (m)")

    plt.axis("equal")
    plt.grid(True)
    plt.legend()

    plt.show()


if __name__ == "__main__":
    run_visual_simulation()