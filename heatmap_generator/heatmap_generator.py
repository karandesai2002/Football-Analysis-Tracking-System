import os
import numpy as np
import matplotlib.pyplot as plt


class HeatmapGenerator:
    def __init__(self, pitch_length=23.32, pitch_width=68):
        self.pitch_length = pitch_length
        self.pitch_width = pitch_width

    def _draw_pitch(self, ax):
        # Pitch outline
        ax.plot([0, 0], [0, self.pitch_width], color="black")
        ax.plot([0, self.pitch_length], [self.pitch_width, self.pitch_width], color="black")
        ax.plot([self.pitch_length, self.pitch_length], [self.pitch_width, 0], color="black")
        ax.plot([self.pitch_length, 0], [0, 0], color="black")

        # Halfway line
        ax.plot([self.pitch_length / 2, self.pitch_length / 2], [0, self.pitch_width], color="black")

        # Center circle
        center_circle = plt.Circle((self.pitch_length / 2, self.pitch_width / 2), 9.15, color="black", fill=False)
        ax.add_patch(center_circle)

        # Left penalty box
        ax.plot([16.5, 16.5], [13.84, self.pitch_width - 13.84], color="black")
        ax.plot([0, 16.5], [13.84, 13.84], color="black")
        ax.plot([0, 16.5], [self.pitch_width - 13.84, self.pitch_width - 13.84], color="black")

        # Right penalty box
        ax.plot([self.pitch_length - 16.5, self.pitch_length - 16.5], [13.84, self.pitch_width - 13.84], color="black")
        ax.plot([self.pitch_length, self.pitch_length - 16.5], [13.84, 13.84], color="black")
        ax.plot([self.pitch_length, self.pitch_length - 16.5], [self.pitch_width - 13.84, self.pitch_width - 13.84], color="black")

        ax.set_xlim(0, self.pitch_length)
        ax.set_ylim(0, self.pitch_width)
        ax.set_aspect("equal")
        ax.axis("off")

    def collect_player_positions(self, tracks):
        player_positions = {}

        for frame_tracks in tracks["players"]:
            for player_id, track_info in frame_tracks.items():
                pos = track_info.get("position_transformed", None)

                if pos is None:
                    continue

                x, y = pos

                if x is None or y is None:
                    continue

                if player_id not in player_positions:
                    player_positions[player_id] = []

                player_positions[player_id].append((x, y))

        return player_positions

    def collect_team_positions(self, tracks):
        team_positions = {1: [], 2: []}

        for frame_tracks in tracks["players"]:
            for player_id, track_info in frame_tracks.items():
                pos = track_info.get("position_transformed", None)
                team = track_info.get("team", None)

                if pos is None or team not in [1, 2]:
                    continue

                x, y = pos

                if x is None or y is None:
                    continue

                team_positions[team].append((x, y))

            return team_positions

    def generate_player_heatmap(self, player_id, positions, output_path):
        if len(positions) == 0:
            return

        positions = np.array(positions)
        x = positions[:, 0]
        y = self.pitch_width-positions[:, 1]

        fig, ax = plt.subplots(figsize=(12, 8))
        self._draw_pitch(ax)

        heatmap, xedges, yedges = np.histogram2d(
            x, y,
            bins=[30, 20],
            range=[[0, self.pitch_length], [0, self.pitch_width]]
        )

        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

        ax.imshow(
            heatmap.T,
            extent=extent,
            origin="lower",
            cmap="hot",
            alpha=0.6,
            aspect="auto"
        )

        ax.set_title(f"Player {player_id} Heatmap", fontsize=16)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()

    def generate_all_player_heatmaps(self, tracks, output_dir="outputs/heatmaps"):
        os.makedirs(output_dir, exist_ok=True)

        player_positions = self.collect_player_positions(tracks)

        for player_id, positions in player_positions.items():
            output_path = os.path.join(output_dir, f"player_{player_id}_heatmap.png")
            self.generate_player_heatmap(player_id, positions, output_path)

    def generate_team_heatmap(self, team_id, positions, output_path):
        if len(positions) == 0:
           return

        positions = np.array(positions)
        x = positions[:, 0]
        y = self.pitch_width - positions[:, 1]

        fig, ax = plt.subplots(figsize=(12, 8))
        self._draw_pitch(ax)

        heatmap, xedges, yedges = np.histogram2d(
            x, y,
            bins=[15, 10],
            range=[[0, self.pitch_length], [0, self.pitch_width]]
        )

        from scipy.ndimage import gaussian_filter
        heatmap = gaussian_filter(heatmap, sigma=2.5)

        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

        ax.imshow(
            heatmap.T,
            extent=extent,
            origin="lower",
            cmap="inferno",
            alpha=0.8,
            aspect="auto"
        )

        ax.set_title(f"Team {team_id} Heatmap", fontsize=16)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()

    def generate_all_team_heatmaps(self, tracks, output_dir="outputs/heatmaps"):
        os.makedirs(output_dir, exist_ok=True)

        team_positions = self.collect_team_positions(tracks)

        for team_id, positions in team_positions.items():
            output_path = os.path.join(output_dir, f"team_{team_id}_heatmap.png")
            self.generate_team_heatmap(team_id, positions, output_path)