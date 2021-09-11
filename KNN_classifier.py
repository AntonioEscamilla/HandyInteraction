###########################################################################################
###                        CODE:       WRITTEN BY: ANTONIO ESCAMILLA                    ###
###                        PROJECT:    HANDY INTERACTION                                ###
###                        PURPOSE:    WINDOWS/LINUX/MACOS FLAT MODERN UI               ###
###                                    BASED ON QT DESIGNER                             ###
###                        LICENCE:    MIT OPENSOURCE LICENCE                           ###
###                                                                                     ###
###                            CODE IS FREE TO USE AND MODIFY                           ###
###########################################################################################

import csv
import numpy as np
import os


class PoseSample(object):

    def __init__(self, landmarks, class_name, embedding):
        self.landmarks = landmarks
        self.class_name = class_name
        self.embedding = embedding


class PoseSampleOutlier(object):

    def __init__(self, sample, detected_class, all_classes):
        self.sample = sample
        self.detected_class = detected_class
        self.all_classes = all_classes


class PoseClassifier(object):
    """Classifies pose landmarks."""

    def __init__(self, pose_samples_folder, pose_embedder, file_extension='csv'):
        self.pose_embedder = pose_embedder
        self.file_extension = file_extension
        self.n_landmarks = 21
        self.n_dimensions = 3
        self.top_n_by_max_distance = 30
        self.top_n_by_mean_distance = 10
        self.axes_weights = (1.0, 1.0, 0.2)

        self.pose_samples = self._load_pose_samples(pose_samples_folder, pose_embedder)
        print(len(self.pose_samples))

    def _load_pose_samples(self, pose_samples_folder, pose_embedder):
        """ Loads pose samples from a given folder."""

        # Each file in the folder represents one pose class.
        file_names = [name for name in os.listdir(pose_samples_folder) if name.endswith(self.file_extension)]

        pose_samples = []
        for file_name in file_names:
            # Use file name as pose class name.
            class_name = file_name[:-(len(self.file_extension) + 1)]

            # Parse CSV.
            with open(os.path.join(pose_samples_folder, file_name)) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                row_counter = 0
                for row in csv_reader:
                    landmarks = np.array(row[:], np.float32).reshape([self.n_landmarks, self.n_dimensions])
                    pose_samples.append(PoseSample(landmarks, class_name, embedding=pose_embedder(landmarks)))
                    row_counter += 1
                    if row_counter == 100:
                        break

        return pose_samples

    def find_pose_sample_outliers(self):
        """Classifies each sample against the entire database."""
        # Find outliers in target poses
        outliers = []
        for sample in self.pose_samples:
            # Find nearest poses for the target one.
            pose_landmarks = sample.landmarks.copy()
            pose_classification = self.__call__(pose_landmarks)
            class_names = [class_name for class_name, count in pose_classification.items() if count == max(pose_classification.values())]

            # Sample is an outlier if nearest poses have different class or more than
            # one pose class is detected as nearest.
            if sample.class_name not in class_names or len(class_names) != 1:
                outliers.append(PoseSampleOutlier(sample, class_names, pose_classification))

        return outliers

    def __call__(self, pose_landmarks):
        """Classifies given pose.

        Classification is done in two stages:
          * First we pick top-N samples by MAX distance. It allows to remove samples
            that are almost the same as given pose, but has few joints bent in the
            other direction.
          * Then we pick top-N samples by MEAN distance. After outliers are removed
            on a previous step, we can pick samples that are closes on average.

        Args:
          pose_landmarks: NumPy array with 3D landmarks of shape (N, 3).

        Returns:
          Dictionary with count of nearest pose samples from the database. Sample:
            {
              'pushups_down': 8,
              'pushups_up': 2,
            }
        """

        # Get given pose embedding.
        pose_embedding = self.pose_embedder(pose_landmarks)
        flipped_pose_embedding = self.pose_embedder(pose_landmarks * np.array([-1, 1, 1]))

        # Filter by max distance.
        #
        # That helps to remove outliers - poses that are almost the same as the
        # given one, but has one joint bent into another direction and actually
        # represnt a different pose class.
        max_dist_heap = []
        for sample_idx, sample in enumerate(self.pose_samples):
            max_dist = min(
                np.max(np.abs(sample.embedding - pose_embedding) * self.axes_weights),
                np.max(np.abs(sample.embedding - flipped_pose_embedding) * self.axes_weights))
            max_dist_heap.append([max_dist, sample_idx])

        max_dist_heap = sorted(max_dist_heap, key=lambda x: x[0])
        max_dist_heap = max_dist_heap[:self.top_n_by_max_distance]

        # Filter by mean distance.
        #
        # After removing outliers we can find the nearest pose by mean distance.
        mean_dist_heap = []
        for _, sample_idx in max_dist_heap:
            sample = self.pose_samples[sample_idx]
            mean_dist = min(
                np.mean(np.abs(sample.embedding - pose_embedding) * self.axes_weights),
                np.mean(np.abs(sample.embedding - flipped_pose_embedding) * self.axes_weights),
            )
            mean_dist_heap.append([mean_dist, sample_idx])

        mean_dist_heap = sorted(mean_dist_heap, key=lambda x: x[0])
        mean_dist_heap = mean_dist_heap[:self.top_n_by_mean_distance]

        # Collect results into map: (class_name -> n_samples)
        class_names = [self.pose_samples[sample_idx].class_name for _, sample_idx in mean_dist_heap]
        result = {class_name: class_names.count(class_name) for class_name in set(class_names)}

        return result


class EMADictSmoothing(object):
    """Smoothes pose classification."""

    def __init__(self, window_size=10, alpha=0.2):
        self._window_size = window_size
        self._alpha = alpha

        self._data_in_window = []

    def __call__(self, data):
        """Smoothes given pose classification.

        Smoothing is done by computing Exponential Moving Average for every pose
        class observed in the given time window. Missed pose classes are replaced
        with 0.

        Args:
          data: Dictionary with pose classification. Sample:
              {
                'pushups_down': 8,
                'pushups_up': 2,
              }

        Result:
          Dictionary in the same format but with smoothed and float instead of
          integer values. Sample:
            {
              'pushups_down': 8.3,
              'pushups_up': 1.7,
            }
        """
        # Add new data to the beginning of the window for simpler code.
        self._data_in_window.insert(0, data)
        self._data_in_window = self._data_in_window[:self._window_size]

        # Get all keys.
        keys = set([key for data in self._data_in_window for key, _ in data.items()])

        # Get smoothed values.
        smoothed_data = dict()
        for key in keys:
            factor = 1.0
            top_sum = 0.0
            bottom_sum = 0.0
            for data in self._data_in_window:
                value = data[key] if key in data else 0.0

                top_sum += factor * value
                bottom_sum += factor

                # Update factor.
                factor *= (1.0 - self._alpha)

            smoothed_data[key] = top_sum / bottom_sum

        return smoothed_data

