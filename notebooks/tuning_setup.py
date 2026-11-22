"""Shared setup for the model tuning notebooks (03_2 onward).

Every tuning notebook imports from here, so all algorithms are tuned and scored the same way:
the same training rows, the same 5 stratified folds, the same scores, the same threshold method,
and the same format for saved results. The consolidation notebook reads those saved results.
"""
import json
import os

import numpy as np
import pandas as pd
from sklearn.metrics import (average_precision_score, f1_score, precision_score,
                             recall_score, roc_auc_score)
from sklearn.model_selection import StratifiedKFold

# Same encoding as 03_baseline_model_testing: best to worst status
STATUS_ORDER = ["Normal", "Delayed", "Disrupted"]
STATUS_TO_NUMBER = {status: number for number, status in enumerate(STATUS_ORDER)}
DISRUPTED = STATUS_TO_NUMBER["Disrupted"]

ID_COLUMNS = ["date", "route_id", "split"]
TARGET_COLUMN = "route_status"

# Threshold candidates for the Disrupted decision (section "Choose the Disrupted Threshold")
THRESHOLDS = np.round(np.arange(0.05, 0.951, 0.01), 2)


def load_training_data(path="../data/preprocessed/model_ready.csv"):
    """Training rows of model_ready.csv as (train_df, X_train, y_train). Test rows are never returned."""
    model_ready_df = pd.read_csv(path)
    model_ready_df["date"] = pd.to_datetime(model_ready_df["date"], format="%m/%d/%Y")

    train_df = model_ready_df[model_ready_df["split"] == "train"].reset_index(drop=True)
    feature_columns = [c for c in model_ready_df.columns if c not in ID_COLUMNS + [TARGET_COLUMN]]

    X_train = train_df[feature_columns]
    y_train = train_df[TARGET_COLUMN].map(STATUS_TO_NUMBER)
    return train_df, X_train, y_train


def make_folds(X, y, n_folds=5):
    """The same stratified folds as 03_baseline_model_testing (shuffle=True, random_state=42)."""
    return list(StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=42).split(X, y))


def disrupted_pr_auc_scorer(estimator, X, y):
    """Disrupted PR-AUC, in the form scikit-learn's search tools accept as a scorer."""
    return average_precision_score(y == DISRUPTED, estimator.predict_proba(X)[:, DISRUPTED])


def best_threshold_macro_f1(y, probabilities, thresholds=THRESHOLDS):
    """macro-F1 with the best Disrupted threshold for these rows (the default rule is one of the options)."""
    y = np.asarray(y)
    options = [None] + list(thresholds)
    return max(f1_score(y, predict_with_threshold(probabilities, t), average="macro") for t in options)


def best_threshold_macro_f1_scorer(estimator, X, y):
    """The score used to pick the best settings in a search.

    Every final model gets its own Disrupted threshold, so settings are compared by the macro-F1 they
    reach with their best threshold, not with the default rule. Otherwise a search mostly rewards
    settings whose default rule happens to fall near a good cut-off (see 03_2 notebooks).
    The threshold is picked on the same rows it is scored on, which is slightly optimistic, but in the
    same way for every combination; section 7 of each notebook gives the honest estimate.
    """
    return best_threshold_macro_f1(y, estimator.predict_proba(X))


# Scores tracked during a hyperparameter search. "macro_f1_best_threshold" picks the best settings
SEARCH_SCORING = {
    "macro_f1_best_threshold": best_threshold_macro_f1_scorer,
    "macro_f1": "f1_macro",                     # with the default rule (highest probability wins)
    "disrupted_pr_auc": disrupted_pr_auc_scorer,
    "roc_auc_ovr": "roc_auc_ovr",
}


def predict_with_threshold(probabilities, threshold=None):
    """Turn probabilities into statuses.

    threshold=None: the default rule (the status with the highest probability wins).
    threshold=t: Disrupted if its probability >= t, otherwise the more likely of Normal and Delayed.
    """
    probabilities = np.asarray(probabilities)
    if threshold is None:
        return probabilities.argmax(axis=1)
    predictions = probabilities[:, :DISRUPTED].argmax(axis=1)
    predictions[probabilities[:, DISRUPTED] >= threshold] = DISRUPTED
    return predictions


def score_predictions(y_true, probabilities, threshold=None):
    """The same scores as 03_baseline_model_testing, for one set of predictions."""
    y_true = np.asarray(y_true)
    probabilities = np.asarray(probabilities)
    predictions = predict_with_threshold(probabilities, threshold)
    per_status_f1 = f1_score(y_true, predictions, average=None, labels=[0, 1, 2])
    return {
        "macro_f1": f1_score(y_true, predictions, average="macro"),
        "f1_normal": per_status_f1[0],
        "f1_delayed": per_status_f1[1],
        "f1_disrupted": per_status_f1[2],
        "disrupted_precision": precision_score(y_true == DISRUPTED, predictions == DISRUPTED, zero_division=0),
        "disrupted_recall": recall_score(y_true == DISRUPTED, predictions == DISRUPTED),
        "disrupted_pr_auc": average_precision_score(y_true == DISRUPTED, probabilities[:, DISRUPTED]),
        "roc_auc_ovr": roc_auc_score(y_true, probabilities, multi_class="ovr", average="macro"),
    }


def score_folds(y, out_of_fold_probabilities, folds, threshold=None):
    """Scores for each fold's held-out rows, from out-of-fold probabilities (one row per fold)."""
    rows = []
    for fold_number, (_, valid_index) in enumerate(folds, start=1):
        scores = score_predictions(np.asarray(y)[valid_index], out_of_fold_probabilities[valid_index], threshold)
        rows.append({"fold": fold_number, **scores})
    return pd.DataFrame(rows).set_index("fold")


def choose_threshold(y, probabilities, thresholds=THRESHOLDS):
    """The threshold with the highest macro-F1 on these rows."""
    y = np.asarray(y)
    macro_f1 = [f1_score(y, predict_with_threshold(probabilities, t), average="macro") for t in thresholds]
    return float(thresholds[int(np.argmax(macro_f1))])


def cross_validated_threshold(y, out_of_fold_probabilities, folds, thresholds=THRESHOLDS):
    """An honest estimate of how a chosen threshold performs on rows it wasn't chosen on.

    For each fold: choose the threshold on the other 4 folds' out-of-fold probabilities,
    then score this fold with it. Returns one row per fold.
    """
    y = np.asarray(y)
    rows = []
    for fold_number, (_, valid_index) in enumerate(folds, start=1):
        other_index = np.setdiff1d(np.arange(len(y)), valid_index)
        threshold = choose_threshold(y[other_index], out_of_fold_probabilities[other_index], thresholds)
        scores = score_predictions(y[valid_index], out_of_fold_probabilities[valid_index], threshold)
        rows.append({"fold": fold_number, "threshold": threshold, **scores})
    return pd.DataFrame(rows).set_index("fold")


def save_tuning_results(model_name, best_params, fold_scores_df, out_of_fold_probabilities, train_df,
                        threshold, search_results_df, results_dir="../results/tuning"):
    """Save one algorithm's tuning results in the shared format the consolidation notebook reads."""
    folder = os.path.join(results_dir, model_name.lower().replace(" ", "_"))
    os.makedirs(folder, exist_ok=True)

    with open(os.path.join(folder, "best_params.json"), "w") as f:
        # .item() turns numpy numbers (e.g. np.int64) into plain Python numbers JSON can store
        json.dump({"model": model_name, "params": best_params, "disrupted_threshold": threshold}, f, indent=2,
                  default=lambda value: value.item() if hasattr(value, "item") else str(value))

    fold_scores_df.to_csv(os.path.join(folder, "cv_fold_scores.csv"))
    search_results_df.to_csv(os.path.join(folder, "search_results.csv"), index=False)

    probabilities_df = train_df[["date", "route_id", TARGET_COLUMN]].copy()
    for number, status in enumerate(STATUS_ORDER):
        probabilities_df[f"prob_{status.lower()}"] = out_of_fold_probabilities[:, number]
    probabilities_df.to_csv(os.path.join(folder, "out_of_fold_probabilities.csv"), index=False, date_format="%m/%d/%Y")

    return folder
