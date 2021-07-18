# Copyright (c) Microsoft Corporation and Fairlearn contributors.
# Licensed under the MIT License.

import pandas as pd
import numpy as np
import pytest
from sklearn.model_selection import train_test_split

from fairlearn.datasets import (
    fetch_adult,
    fetch_boston,
    fetch_bank_marketing,
    make_synthetic_dataset,
)

# =============================================


class TestFairlearnDataset:

    @pytest.mark.parametrize("as_frame", [True, False])
    @pytest.mark.parametrize("fetch_function", [fetch_adult, fetch_boston, fetch_bank_marketing])
    def test_dataset_as_bunch(self, as_frame, fetch_function):
        dataset = fetch_function(as_frame=as_frame)
        assert dataset is not None
        assert dataset['data'].shape is not None
        assert isinstance(dataset['data'], pd.DataFrame if as_frame else np.ndarray)
        assert dataset['target'].shape is not None
        assert isinstance(dataset['target'], pd.Series if as_frame else np.ndarray)
        assert dataset['feature_names'] is not None
        assert isinstance(dataset['feature_names'], list)
        assert dataset['DESCR'] is not None
        assert isinstance(dataset['DESCR'], str)

    @pytest.mark.parametrize("as_frame", [True, False])
    @pytest.mark.parametrize("fetch_function", [fetch_adult, fetch_boston, fetch_bank_marketing])
    def test_dataset_as_X_y(self, as_frame, fetch_function):
        X, y = fetch_function(as_frame=as_frame, return_X_y=True)
        assert X is not None
        assert isinstance(X, pd.DataFrame if as_frame else np.ndarray)
        assert y is not None
        assert isinstance(y, pd.Series if as_frame else np.ndarray)

    def test_simple_synthetic_dataset(self):
        """Ensure that dataset creation is deterministic."""
        rng = np.random.RandomState(54321)
        X, y, gender = make_synthetic_dataset(random_state=rng)

        counts = [250, 251, 249, 251]
        for i in range(4):
            assert np.sum(y[i*500:(i+1)*500]) == counts[i]

        assert np.isclose(np.mean(X), 0.012162)
        assert X.shape == (2000, 20)
        assert y.shape == (2000,)
        assert gender.shape == (2000,)
