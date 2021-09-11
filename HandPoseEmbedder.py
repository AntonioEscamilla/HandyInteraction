###########################################################################################
###                        CODE:       WRITTEN BY: ANTONIO ESCAMILLA                    ###
###                        PROJECT:    HANDY INTERACTION                                ###
###                        PURPOSE:    WINDOWS/LINUX/MACOS FLAT MODERN UI               ###
###                                    BASED ON QT DESIGNER                             ###
###                        LICENCE:    MIT OPENSOURCE LICENCE                           ###
###                                                                                     ###
###                            CODE IS FREE TO USE AND MODIFY                           ###
###########################################################################################

import numpy as np


class HandPoseEmbedder(object):
    """Converts 3D pose landmarks into 3D embedding."""

    def __init__(self, palm_size_multiplier=2.5):
        # Multiplier to apply to the palm to get minimal hand size.
        self._palm_size_multiplier = palm_size_multiplier
        self._previous_pose_center = None
        self._previous_pose_size = None
        self._previous_pose_angle = None

        # Names of the landmarks as they appear in the prediction.
        self._landmark_names = [
            'WRIST',
            'THUMB_CMC', 'THUMB_MCP', 'THUMB_IP', 'THUMB_TIP',
            'INDEX_FINGER_MCP', 'INDEX_FINGER_PIP', 'INDEX_FINGER_DIP', 'INDEX_FINGER_TIP',
            'MIDDLE_FINGER_MCP', 'MIDDLE_FINGER_PIP', 'MIDDLE_FINGER_DIP', 'MIDDLE_FINGER_TIP',
            'RING_FINGER_MCP', 'RING_FINGER_PIP', 'RING_FINGER_DIP', 'RING_FINGER_TIP',
            'PINKY_MCP', 'PINKY_PIP', 'PINKY_DIP', 'PINKY_TIP',
        ]

    def __call__(self, landmarks):
        """Normalizes pose landmarks and converts to embedding

        Args:
          landmarks - NumPy array with 3D landmarks of shape (N, 3).

        Result:
          Numpy array with pose embedding of shape (M, 3) where `M` is the number of
          pairwise distances defined in `_get_pose_distance_embedding`.
        """
        # Get pose landmarks.
        landmarks = np.copy(landmarks)

        # Normalize landmarks.
        landmarks = self.normalize_pose_landmarks(landmarks)

        # Get embedding.
        embedding = self._get_pose_distance_embedding(landmarks)

        return embedding

    def normalize_pose_landmarks(self, landmarks):
        """Normalizes landmarks translation and scale."""
        landmarks = np.copy(landmarks)

        # Normalize translation.
        pose_center = self._get_pose_center(landmarks)
        landmarks -= pose_center

        # Normalize scale.
        pose_size = self._get_pose_size(landmarks, self._palm_size_multiplier)
        landmarks /= pose_size

        return landmarks

    def get_center_and_size(self, landmarks):
        landmarks = np.copy(landmarks)
        landmarks = self.get_landmarks_2dArray(landmarks)
        landmarks = landmarks[:, :2]

        pose_center = np.round(self._get_pose_center(landmarks), 3)
        pose_size = np.round(self._get_pose_size(landmarks, 0.8), 4)
        features = {'Hand center x': pose_center[0], 'Hand center y': pose_center[1], 'Hand size': pose_size}
        return features

    def scroll_direction(self, landmarks):
        landmarks = np.copy(landmarks)
        landmarks = self.get_landmarks_2dArray(landmarks)
        landmarks = landmarks[:, :2]                    # This approach uses only 2D landmarks

        angle = state = None
        pose_center = self._get_pose_center(landmarks)
        if not (self._previous_pose_center is None):
            movement_distance = self._get_distance_norm(pose_center, self._previous_pose_center)
            movement_distance_factor = 0.02

            movement_distance_threshold = movement_distance_factor * self._get_pose_size(landmarks, self._palm_size_multiplier)
            if movement_distance > movement_distance_threshold:
                angle = np.round(self._get_scroll_angle(pose_center, self._previous_pose_center), 2)
                if -45 <= angle < 45:
                    state = 'Scrolling right'
                elif 45 <= angle < 135:
                    state = 'Scrolling up'
                elif angle >= 135 or angle < -135:
                    state = 'Scrolling left'
                elif -135 <= angle < -45:
                    state = 'Scrolling down'
        self._previous_pose_center = pose_center
        features = {'Moving direction': angle, 'Hand state': state}
        return features

    def zoom_direction(self, landmarks):
        landmarks = np.copy(landmarks)
        landmarks = self.get_landmarks_2dArray(landmarks)
        pose_size = np.round(self._get_pose_size(landmarks, 0.8), 4)

        state = None
        if not (self._previous_pose_size is None):
            size_difference_factor = 0.01
            size_difference_threshold = pose_size * size_difference_factor

            if pose_size < (self._previous_pose_size - size_difference_threshold):
                state = 'Zoom out'
            elif pose_size > (self._previous_pose_size + size_difference_threshold):
                state = 'Zoom in'
        self._previous_pose_size = pose_size
        features = {'Hand size': pose_size, 'Hand state': state}
        return features

    def slide_direction(self, landmarks):
        landmarks = np.copy(landmarks)
        landmarks = self.get_landmarks_2dArray(landmarks)
        pose_angle = np.round(self._get_hand_orientation(landmarks), 2)

        state = None
        if not (self._previous_pose_angle is None):
            angle_difference_threshold = 9
            if 80 <= self._previous_pose_angle <= 100:
                if pose_angle > (self._previous_pose_angle + angle_difference_threshold):
                    state = 'Slide left'
                    self._previous_pose_angle = None
                    features = {'Hand orientation': pose_angle, 'Hand state': state}
                    return features

                elif pose_angle < (self._previous_pose_angle - angle_difference_threshold):
                    state = 'Slide right'
                    self._previous_pose_angle = None
                    features = {'Hand orientation': pose_angle, 'Hand state': state}
                    return features

        self._previous_pose_angle = pose_angle
        features = {'Hand orientation': pose_angle, 'Hand state': state}
        return features

    def _get_pose_distance_embedding(self, landmarks):
        """Converts pose landmarks into 3D embedding.

        We use several pairwise 3D distances to form pose embedding. All distances
        include X and Y components with sign. We differnt types of pairs to cover
        different pose classes. Feel free to remove some or add new.

        Args:
          landmarks - NumPy array with 3D landmarks of shape (N, 3).

        Result:
          Numpy array with pose embedding of shape (M, 3) where `M` is the number of
          pairwise distances.
        """
        embedding = np.array([
            # One joint.
            self._get_distance_by_names(landmarks, 'THUMB_TIP', 'THUMB_MCP'),
            self._get_distance_by_names(landmarks, 'INDEX_FINGER_TIP', 'INDEX_FINGER_MCP'),
            self._get_distance_by_names(landmarks, 'MIDDLE_FINGER_TIP', 'MIDDLE_FINGER_MCP'),
            self._get_distance_by_names(landmarks, 'RING_FINGER_TIP', 'RING_FINGER_MCP'),
            self._get_distance_by_names(landmarks, 'PINKY_TIP', 'PINKY_MCP'),

            self._get_distance_by_names(landmarks, 'THUMB_TIP', 'THUMB_IP'),
            self._get_distance_by_names(landmarks, 'INDEX_FINGER_TIP', 'INDEX_FINGER_PIP'),
            self._get_distance_by_names(landmarks, 'MIDDLE_FINGER_TIP', 'MIDDLE_FINGER_PIP'),
            self._get_distance_by_names(landmarks, 'RING_FINGER_TIP', 'RING_FINGER_PIP'),
            self._get_distance_by_names(landmarks, 'PINKY_TIP', 'PINKY_PIP'),

            # Two joints.
            self._get_distance_by_names(landmarks, 'THUMB_TIP', 'INDEX_FINGER_TIP'),
            self._get_distance_by_names(landmarks, 'THUMB_TIP', 'MIDDLE_FINGER_TIP'),
            self._get_distance_by_names(landmarks, 'THUMB_TIP', 'RING_FINGER_TIP'),
            self._get_distance_by_names(landmarks, 'THUMB_TIP', 'PINKY_TIP'),

            self._get_distance_by_names(landmarks, 'INDEX_FINGER_TIP', 'MIDDLE_FINGER_TIP'),
            self._get_distance_by_names(landmarks, 'INDEX_FINGER_TIP', 'RING_FINGER_TIP'),
            self._get_distance_by_names(landmarks, 'INDEX_FINGER_TIP', 'PINKY_TIP'),

            self._get_distance_by_names(landmarks, 'MIDDLE_FINGER_TIP', 'RING_FINGER_TIP'),
            self._get_distance_by_names(landmarks, 'MIDDLE_FINGER_TIP', 'PINKY_TIP'),

            self._get_distance_by_names(landmarks, 'RING_FINGER_TIP', 'PINKY_TIP'),

            # Four joints.
            self._get_distance_by_names(landmarks, 'WRIST', 'INDEX_FINGER_TIP'),
            self._get_distance_by_names(landmarks, 'WRIST', 'MIDDLE_FINGER_TIP'),
            self._get_distance_by_names(landmarks, 'WRIST', 'RING_FINGER_TIP'),
            self._get_distance_by_names(landmarks, 'WRIST', 'PINKY_TIP'),

            # Five joints.
            self._get_distance_by_names(landmarks, 'THUMB_TIP', 'MIDDLE_FINGER_MCP'),

            # Body bent direction.
            # self._get_hand_orientation(landmarks)
        ])

        return embedding

    def _get_pose_center(self, landmarks):
        embedding = np.array([
            self._get_distance_norm_by_names(landmarks, 'WRIST', 'THUMB_TIP'),
            self._get_distance_norm_by_names(landmarks, 'WRIST', 'INDEX_FINGER_TIP'),
            self._get_distance_norm_by_names(landmarks, 'WRIST', 'MIDDLE_FINGER_TIP'),
            self._get_distance_norm_by_names(landmarks, 'WRIST', 'RING_FINGER_TIP'),
            self._get_distance_norm_by_names(landmarks, 'WRIST', 'PINKY_TIP')])
        max_wrist_tip_distance = np.max(embedding)
        tip_idx = 4 * (np.argmax(embedding) + 1)

        if max_wrist_tip_distance > self._get_distance_norm_by_names(landmarks, 'WRIST', 'MIDDLE_FINGER_MCP'):
            px_1 = landmarks[self._landmark_names.index('WRIST')]
            px_2 = landmarks[tip_idx]
        else:
            px_1 = landmarks[self._landmark_names.index('WRIST')]
            px_2 = landmarks[self._landmark_names.index('MIDDLE_FINGER_MCP')]
        center = (px_1 + px_2) * 0.5
        return center

    def _get_pose_size(self, landmarks, palm_size_multiplier):
        """Calculates pose size.

        It is the maximum of two values:
          * Palm size multiplied by `palm_size_multiplier`
          * Maximum distance from pose center to any pose landmark
        """
        # This approach uses only 2D landmarks to compute pose size.
        landmarks = landmarks[:, :2]

        # Palm size as the minimum body size.
        wrist = landmarks[self._landmark_names.index('WRIST')]
        middle_mcp = landmarks[self._landmark_names.index('MIDDLE_FINGER_MCP')]
        palm_size = np.linalg.norm(wrist - middle_mcp)

        # Max dist to pose center.
        pose_center = self._get_pose_center(landmarks)
        max_dist = np.max(np.linalg.norm(landmarks - pose_center, axis=1))

        return max(palm_size * palm_size_multiplier, max_dist)

    def _get_distance_by_names(self, landmarks, name_from, name_to):
        lmk_from = landmarks[self._landmark_names.index(name_from)]
        lmk_to = landmarks[self._landmark_names.index(name_to)]
        return self._get_distance(lmk_from, lmk_to)

    def _get_distance_norm_by_names(self, landmarks, name_from, name_to):
        lmk_from = landmarks[self._landmark_names.index(name_from)]
        lmk_to = landmarks[self._landmark_names.index(name_to)]
        return self._get_distance_norm(lmk_from, lmk_to)

    def _get_hand_orientation(self, landmarks):
        """
            https://stackoverflow.com/questions/35176451/python-code-to-calculate-angle-between-three-point-using-their-3d-coordinates
            a, b and c : points as np.array([x, y, z])
        """
        a = landmarks[self._landmark_names.index('MIDDLE_FINGER_MCP')]
        b = landmarks[self._landmark_names.index('WRIST')]
        c = landmarks[self._landmark_names.index('WRIST')] + np.array([0.1, 0, 0])
        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)
        return np.degrees(angle)

    @staticmethod
    def _get_scroll_angle(actual_pos, prev_pos):
        c = prev_pos + np.array([0.1, 0])

        ab = prev_pos - actual_pos
        cb = prev_pos - c
        dot = (ab[0] * cb[0] + ab[1] * cb[1])       # dot product
        cross = (ab[0] * cb[1] - ab[1] * cb[0])     # cross product
        alpha = np.arctan2(cross, dot)
        return np.degrees(alpha)

    @staticmethod
    def _get_distance_norm(lmk_from, lmk_to):
        return np.linalg.norm(lmk_to - lmk_from)

    @staticmethod
    def _get_distance(lmk_from, lmk_to):
        return lmk_to - lmk_from

    @staticmethod
    def get_landmarks_2dArray(landmarks):
        """ output array of size (21, 3) """
        a_list = []
        for j in range(21):
            a_list.append(np.array([landmarks[j].x, landmarks[j].y, landmarks[j].z]))
        return np.array(a_list)

    @staticmethod
    def get_landmarks_array(landmarks):
        """ output array of size (1, 63) """
        landmarks_list = []
        for j in range(21):
            landmarks_list.append(landmarks[j].x)
            landmarks_list.append(landmarks[j].y)
            landmarks_list.append(landmarks[j].z)
        return np.array(landmarks_list).reshape((1, 63))

    @staticmethod
    def get_landmarks_list(landmarks):
        landmarks_list = []
        for j in range(21):
            landmarks_list.append(landmarks[j].x)
            landmarks_list.append(landmarks[j].y)
            landmarks_list.append(landmarks[j].z)
        return landmarks_list

    @staticmethod
    def get_xy_landmarks_2dArray(landmarks):
        """ output array of size (21, 2) """
        a_list = []
        for j in range(21):
            a_list.append(np.array([landmarks[j].x, landmarks[j].y]))
        return np.array(a_list)

    @staticmethod
    def get_structured_landmarks(landmarks):
        structured_landmarks = []
        for j in range(21):
            structured_landmarks.append(np.array([landmarks[j].x, landmarks[j].y, landmarks[j].z]))
        return structured_landmarks
