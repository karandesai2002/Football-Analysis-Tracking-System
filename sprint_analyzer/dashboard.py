import os
import matplotlib.pyplot as plt


class AnalyticsDashboard:
    def __init__(self):
        pass

    def plot_dashboard(self, player_stats, output_path="outputs/analytics_dashboard.png"):
        os.makedirs("outputs", exist_ok=True)

        sorted_speed = sorted(
            player_stats.items(),
            key=lambda x: x[1]["max_speed"],
            reverse=True
        )[:5]

        sorted_distance = sorted(
            player_stats.items(),
            key=lambda x: x[1]["total_distance"],
            reverse=True
        )[:5]

        sorted_sprints = sorted(
            player_stats.items(),
            key=lambda x: x[1]["sprint_count"],
            reverse=True
        )[:5]

        fig, axes = plt.subplots(1, 3, figsize=(18, 5))

        # Max speed
        speed_ids = [str(x[0]) for x in sorted_speed]
        speed_vals = [x[1]["max_speed"] for x in sorted_speed]
        axes[0].bar(speed_ids, speed_vals)
        axes[0].set_title("Top 5 Max Speeds")
        axes[0].set_xlabel("Player ID")
        axes[0].set_ylabel("km/h")

        # Distance
        dist_ids = [str(x[0]) for x in sorted_distance]
        dist_vals = [x[1]["total_distance"] for x in sorted_distance]
        axes[1].bar(dist_ids, dist_vals)
        axes[1].set_title("Top 5 Distance Covered")
        axes[1].set_xlabel("Player ID")
        axes[1].set_ylabel("m")

        # Sprints
        sprint_ids = [str(x[0]) for x in sorted_sprints]
        sprint_vals = [x[1]["sprint_count"] for x in sorted_sprints]
        axes[2].bar(sprint_ids, sprint_vals)
        axes[2].set_title("Top 5 Sprint Counts")
        axes[2].set_xlabel("Player ID")
        axes[2].set_ylabel("count")

        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()