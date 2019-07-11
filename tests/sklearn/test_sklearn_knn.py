# -*- coding: utf-8 -*-
import sys
sys.path.insert(0,'..')

import numpy as np
import sklearn
from sklearn.datasets import load_iris, load_boston
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

from ceml.sklearn import generate_counterfactual


def test_knn_classifier():
    # Load data
    X, y = load_iris(True)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=4242)

    # Create and fit model
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X_train, y_train)

    # Select data point for explaining its prediction
    x_orig = X_test[1:4][0,:]
    assert model.predict([x_orig]) == 2

    # Compute counterfactual
    features_whitelist = None

    x_cf, y_cf, delta = generate_counterfactual(model, x_orig, 0, features_whitelist=features_whitelist, regularization="l1", C=1.0, optimizer="bfgs", return_as_dict=False)
    assert y_cf == 0
    assert model.predict(np.array([x_cf])) == 0

    x_cf, y_cf, delta = generate_counterfactual(model, x_orig, 0, features_whitelist=features_whitelist, regularization="l1", C=1.0, optimizer="nelder-mead", return_as_dict=False)
    assert y_cf == 0
    assert model.predict(np.array([x_cf])) == 0

    x_cf, y_cf, delta = generate_counterfactual(model, x_orig, 0, features_whitelist=features_whitelist, regularization=None, optimizer="bfgs", return_as_dict=False)
    assert y_cf == 0
    assert model.predict(np.array([x_cf])) == 0

    x_cf, y_cf, delta = generate_counterfactual(model, x_orig, 0, features_whitelist=features_whitelist, regularization=None, optimizer="nelder-mead", return_as_dict=False)
    assert y_cf == 0
    assert model.predict(np.array([x_cf])) == 0


    features_whitelist = [0, 2]
    #x_cf, y_cf, delta = generate_counterfactual(model, x_orig, 0, features_whitelist=features_whitelist, regularization="l2", C=1.0, optimizer="bfgs", return_as_dict=False)
    #assert y_cf == 0
    #assert model.predict(np.array([x_cf])) == 0
    #assert all([True if i in features_whitelist else delta[i] == 0. for i in range(x_orig.shape[0])])

    x_cf, y_cf, delta = generate_counterfactual(model, x_orig, 0, features_whitelist=features_whitelist, regularization="l1", C=1.0, optimizer="nelder-mead", return_as_dict=False)
    assert y_cf == 0
    assert model.predict(np.array([x_cf])) == 0
    assert all([True if i in features_whitelist else delta[i] == 0. for i in range(x_orig.shape[0])])

    #x_cf, y_cf, delta = generate_counterfactual(model, x_orig, 0, features_whitelist=features_whitelist, regularization=None, optimizer="bfgs", return_as_dict=False)
    #assert y_cf == 0
    #assert model.predict(np.array([x_cf])) == 0
    #assert all([True if i in features_whitelist else delta[i] == 0. for i in range(x_orig.shape[0])])

    x_cf, y_cf, delta = generate_counterfactual(model, x_orig, 0, features_whitelist=features_whitelist, regularization=None, optimizer="nelder-mead", return_as_dict=False)
    assert y_cf == 0
    assert model.predict(np.array([x_cf])) == 0
    assert all([True if i in features_whitelist else delta[i] == 0. for i in range(x_orig.shape[0])])


def test_knn_regressor():
    # Load data
    X, y = load_boston(True)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=4242)

    # Create and fit model
    model = KNeighborsRegressor(n_neighbors=3)
    model.fit(X_train, y_train)

    # Select data point for explaining its prediction
    x_orig = X_test[1:4][0,:]
    y_orig_pred = model.predict([x_orig])
    assert y_orig_pred >= 20. and y_orig_pred <= 21.

    # Compute counterfactual
    y_target = 25.
    y_target_done = lambda z: np.abs(z - y_target) < 2.

    features_whitelist = None

    x_cf, y_cf, delta = generate_counterfactual(model, x_orig, y_target, done=y_target_done, features_whitelist=features_whitelist, regularization="l1", C=1.0, optimizer="bfgs", return_as_dict=False)
    assert y_target_done(y_cf)
    assert y_target_done(model.predict(np.array([x_cf])))

    x_cf, y_cf, delta = generate_counterfactual(model, x_orig, y_target, done=y_target_done, features_whitelist=features_whitelist, regularization="l1", C=1.0, optimizer="nelder-mead", return_as_dict=False)
    assert y_target_done(y_cf)
    assert y_target_done(model.predict(np.array([x_cf])))

    x_cf, y_cf, delta = generate_counterfactual(model, x_orig, y_target, done=y_target_done, features_whitelist=features_whitelist, regularization=None, optimizer="bfgs", return_as_dict=False)
    assert y_target_done(y_cf)
    assert y_target_done(model.predict(np.array([x_cf])))

    x_cf, y_cf, delta = generate_counterfactual(model, x_orig, y_target, done=y_target_done, features_whitelist=features_whitelist, regularization=None, optimizer="nelder-mead", return_as_dict=False)
    assert y_target_done(y_cf)
    assert y_target_done(model.predict(np.array([x_cf])))


    features_whitelist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    x_cf, y_cf, delta = generate_counterfactual(model, x_orig, y_target, done=y_target_done, features_whitelist=features_whitelist, regularization="l1", C=1.0, optimizer="bfgs", return_as_dict=False)
    assert y_target_done(y_cf)
    assert y_target_done(model.predict(np.array([x_cf])))
    assert all([True if i in features_whitelist else delta[i] == 0. for i in range(x_orig.shape[0])])

    x_cf, y_cf, delta = generate_counterfactual(model, x_orig, y_target, done=y_target_done, features_whitelist=features_whitelist, regularization="l1", C=1.0, optimizer="nelder-mead", return_as_dict=False)
    assert y_target_done(y_cf)
    assert y_target_done(model.predict(np.array([x_cf])))
    assert all([True if i in features_whitelist else delta[i] == 0. for i in range(x_orig.shape[0])])

    x_cf, y_cf, delta = generate_counterfactual(model, x_orig, y_target, done=y_target_done, features_whitelist=features_whitelist, regularization=None, optimizer="bfgs", return_as_dict=False)
    assert y_target_done(y_cf)
    assert y_target_done(model.predict(np.array([x_cf])))
    assert all([True if i in features_whitelist else delta[i] == 0. for i in range(x_orig.shape[0])])

    x_cf, y_cf, delta = generate_counterfactual(model, x_orig, y_target, done=y_target_done, features_whitelist=features_whitelist, regularization=None, optimizer="nelder-mead", return_as_dict=False)
    assert y_target_done(y_cf)
    assert y_target_done(model.predict(np.array([x_cf])))
    assert all([True if i in features_whitelist else delta[i] == 0. for i in range(x_orig.shape[0])])