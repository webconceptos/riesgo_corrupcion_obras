from functools import lru_cache

import numpy as np
import pandas as pd
import shap


def split_estimator(pipeline):
    """Devuelve (preprocesador_o_None, estimador_final). Mismo patrón que demo/demo_app.py."""
    if hasattr(pipeline, "steps"):
        steps = [s for _, s in pipeline.steps]
        return (pipeline[:-1] if len(steps) > 1 else None), steps[-1]
    return None, pipeline


@lru_cache(maxsize=4)
def _get_explainer(pipeline) -> shap.TreeExplainer:
    _, estimator = split_estimator(pipeline)
    return shap.TreeExplainer(estimator)


def compute_top_contributions(
    pipeline, X: pd.DataFrame, predicted_class: int, top_n: int = 12
) -> list[dict]:
    pre, _ = split_estimator(pipeline)
    explainer = _get_explainer(pipeline)

    Xt = pre.transform(X) if pre is not None else X.values
    try:
        names = list(pre.get_feature_names_out())
    except Exception:
        names = list(X.columns)

    shap_values = explainer.shap_values(Xt)
    if isinstance(shap_values, list):
        sv_cls = shap_values[predicted_class]
    elif np.ndim(shap_values) == 3:
        sv_cls = shap_values[:, :, predicted_class]
    else:
        sv_cls = shap_values

    vals = np.array(sv_cls).reshape(-1)
    order = np.argsort(np.abs(vals))[::-1][:top_n]

    return [
        {
            "feature": str(names[i]).replace("num__", "").replace("cat__", ""),
            "shap_value": float(vals[i]),
        }
        for i in order
    ]
