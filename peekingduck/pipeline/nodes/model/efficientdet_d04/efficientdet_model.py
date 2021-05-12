"""
Copyright 2021 AI Singapore

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import logging
from typing import Dict, Any, List, Tuple
import json
import numpy as np

from peekingduck.weights_utils import checker, downloader
from peekingduck.pipeline.nodes.model.efficientdet_d04.efficientdet_files.detector import Detector


class EfficientDetModel:
    """EfficientDet model with model types: D0-D4"""

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__()

        self.logger = logging.getLogger(__name__)
        # check for efficientdet weights, if none then download into weights folder
        if not checker.has_weights(config['root'],
                                   config['weights_dir']):
            self.logger.info('---no efficientdet weights detected. proceeding to download...---')
            downloader.download_weights(config['root'],
                                        config['weights_id'])
            self.logger.info('---efficientdet weights download complete.---')

        # get classnames path to read all the classes
        classes_path = os.path.join(config['root'], config['classes'])
        self.class_names = {value['id'] - 1: value['name']
                            for value in json.load(open(classes_path, 'r')).values()}
        self.detect_ids = config['detect_ids']
        self.logger.info('efficientdet model detecting ids: %s', self.detect_ids)

        self.detector = Detector(config)

    def predict(self, frame: List[List[float]]) -> Tuple[List, List, List]:
        """predict the bbox from frame

        returns:
        object_bboxes(List[Numpy Array]): list of bboxes detected
        object_labels(List[int]): list of index labels of the
            object detected for the corresponding bbox
        object_scores(List(float)): list of confidence scores of the
            object detected for the corresponding bbox
        """
        assert isinstance(frame, np.ndarray)

        # return bboxes, object_bboxes, object_labels, object_scores
        return self.detector.predict_bbox_from_image(frame, self.detect_ids)

    def get_detect_ids(self) -> None:
        """getter function for ids to be detected
        """
        return self.detect_ids
