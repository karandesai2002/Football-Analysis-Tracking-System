from sklearn.cluster import KMeans
import numpy as np

class TeamAssigner:
    def __init__(self):
        self.team_colors={}
        self.player_team_dict={}


    def get_clustering_model(self, image):
        #Reshape the image to 2D array
        image_2d=image.reshape(-1,3)

        #Perform KMeanswith 2 clusters
        kmeans=KMeans(n_clusters=2, random_state=0, init="k-means++", n_init=1).fit(image_2d)

        return kmeans

    def get_player_color(self, frame, bbox):
         x1, y1, x2, y2 = map(int, bbox)

         h, w = frame.shape[:2]
         x1 = max(0, x1)
         y1 = max(0, y1)
         x2 = min(w, x2)
         y2 = min(h, y2)

         if x2 <= x1 or y2 <= y1:
           return np.array([0, 0, 0], dtype=np.float32)

         image = frame[y1:y2, x1:x2]

         if image.size == 0 or image.shape[0] < 2 or image.shape[1] < 2:
           return np.array([0, 0, 0], dtype=np.float32)

         top_half_image = image[: image.shape[0] // 2, :]

         if top_half_image.size == 0 or top_half_image.shape[0] < 2 or top_half_image.shape[1] < 2:
           return np.array([0, 0, 0], dtype=np.float32)

         image_2d = top_half_image.reshape(-1, 3).astype(np.float32)

        # If all pixels are nearly identical, KMeans is unnecessary
         if len(np.unique(image_2d, axis=0)) < 2:
            return image_2d.mean(axis=0)

         kmeans = KMeans(n_clusters=2, random_state=0, init="k-means++", n_init=10)
         kmeans.fit(image_2d)
        
         #Get the Cluster Labels for each pixel
         labels=kmeans.labels_

         #Reshape the labels to the image shape
         clustered_image=labels.reshape(top_half_image.shape[0], top_half_image.shape[1])

         #Get the player cluster
         corner_clusters=[clustered_image[0,0], clustered_image[0,-1], clustered_image[-1,0], clustered_image[-1,-1]]
         non_player_cluster=max(set(corner_clusters), key=corner_clusters.count)
         player_cluster=1-non_player_cluster

         player_color=np.array(kmeans.cluster_centers_[player_cluster], dtype=np.float32).flatten()

         return player_color

    def assign_team_color(self, frame, player_detections):

        player_colors=[]
        for _,player_detection in player_detections.items():
            bbox=player_detection['bbox']
            player_color=self.get_player_color(frame,bbox)

            if np.all(player_color == 0):
                continue
            player_colors.append(player_color)

        if len(player_colors) < 2:
            raise ValueError(f"Need at least 2 valid player colors, got {len(player_colors)}")    

        player_colors = np.array(player_colors, dtype=np.float32)    
        kmeans=KMeans(n_clusters=2, init="k-means++", n_init=1).fit(player_colors)

        self.kmeans=kmeans

        self.team_colors[1]=kmeans.cluster_centers_[0]
        self.team_colors[2]=kmeans.cluster_centers_[1]

    def get_player_team(self, frame, player_bbox, player_id):
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]

        player_color=self.get_player_color(frame, player_bbox)

        print("player_color:", player_color)
        print("type:", type(player_color))
        print("shape:", player_color.shape)

        player_color = np.array(player_color, dtype=np.float32)
        team_id=self.kmeans.predict(player_color.reshape(1,-1))[0]
        team_id+=1
              
        self.player_team_dict[player_id]=team_id

        return team_id       