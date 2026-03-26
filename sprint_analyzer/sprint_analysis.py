import os
import matplotlib.pyplot as plt


class SprintAnalyzer:
    def __init__(self):
        pass

    def compute_player_stats(self, tracks):
        player_stats = {}

        for frame_tracks in tracks["players"]:
            for player_id, track in frame_tracks.items():

                speed = track.get("speed", 0)
                distance = track.get("distance", 0)

                if player_id not in player_stats:
                    player_stats[player_id] = {
                        "max_speed": 0,
                        "total_distance": 0,
                        "sprint_count": 0
                    }

                # Max speed
                if speed > player_stats[player_id]["max_speed"]:
                    player_stats[player_id]["max_speed"] = speed

                # Distance
                player_stats[player_id]["total_distance"] = distance

                # Sprint condition (you can tweak threshold)
                if speed > 25:
                    player_stats[player_id]["sprint_count"] += 1

        return player_stats

    def plot_top_speeds(self, player_stats, output_path="outputs/top_speeds.png"):
        os.makedirs("outputs", exist_ok=True)

        players = list(player_stats.keys())
        speeds = [player_stats[p]["max_speed"] for p in players]

        # Sort
        sorted_data = sorted(zip(players, speeds), key=lambda x: x[1], reverse=True)
        top_players = [str(p[0]) for p in sorted_data[:5]]
        top_speeds = [p[1] for p in sorted_data[:5]]

        plt.figure(figsize=(8, 5))
        plt.bar(top_players, top_speeds)
        plt.xlabel("Player ID")
        plt.ylabel("Max Speed (km/h)")
        plt.title("Top 5 Fastest Players")

        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()