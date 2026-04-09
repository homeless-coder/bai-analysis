from __future__ import annotations

import sys
from pathlib import Path
from textwrap import wrap

import pandas as pd


CATEGORY_ORDER = ["LOW", "MODERATE", "SEVERE"]
CATEGORY_PALETTE = {
    "LOW": "#2A9D8F",
    "MODERATE": "#F4A261",
    "SEVERE": "#C1121F",
}
GENDER_PALETTE = {
    "M": "#457B9D",
    "F": "#E76F51",
}
CLUSTER_PALETTE = ["#264653", "#2A9D8F", "#E76F51", "#457B9D", "#F4A261", "#8D99AE"]
SCORE_BANDS = [
    (0, 21, "LOW", "#D9F0EA"),
    (22, 35, "MODERATE", "#FDE4C8"),
    (36, 63, "SEVERE", "#FAD0C8"),
]

BAI_SYMPTOMS = {
    "BAI_1": "Entumecimiento u hormigueo",
    "BAI_2": "Sensación de calor",
    "BAI_3": "Temblor en las piernas",
    "BAI_4": "Incapacidad para relajarse",
    "BAI_5": "Miedo a que ocurra lo peor",
    "BAI_6": "Mareo o aturdimiento",
    "BAI_7": "Latidos fuertes o rápidos",
    "BAI_8": "Inestabilidad",
    "BAI_9": "Terror o miedo",
    "BAI_10": "Nerviosismo",
    "BAI_11": "Sensación de ahogo",
    "BAI_12": "Temblor en las manos",
    "BAI_13": "Temblor general",
    "BAI_14": "Miedo a perder el control",
    "BAI_15": "Dificultad para respirar",
    "BAI_16": "Miedo a morir",
    "BAI_17": "Asustado",
    "BAI_18": "Indigestión o malestar abdominal",
    "BAI_19": "Sensación de desmayo",
    "BAI_20": "Rubor facial",
    "BAI_21": "Sudoración",
}
BAI_SHORT_SYMPTOMS = {
    "BAI_1": "Hormigueo",
    "BAI_2": "Calor",
    "BAI_3": "Piernas temblorosas",
    "BAI_4": "No puede relajarse",
    "BAI_5": "Miedo a lo peor",
    "BAI_6": "Mareo",
    "BAI_7": "Latidos rápidos",
    "BAI_8": "Inestabilidad",
    "BAI_9": "Terror o miedo",
    "BAI_10": "Nerviosismo",
    "BAI_11": "Ahogo",
    "BAI_12": "Manos temblorosas",
    "BAI_13": "Temblor general",
    "BAI_14": "Perder control",
    "BAI_15": "Dificultad respiratoria",
    "BAI_16": "Miedo a morir",
    "BAI_17": "Asustado",
    "BAI_18": "Indigestión",
    "BAI_19": "Desmayo",
    "BAI_20": "Rubor facial",
    "BAI_21": "Sudoración",
}


def add_project_root_to_path(current_path: str | Path | None = None) -> Path:
    """Agrega la raiz del proyecto a sys.path y retorna la ruta resuelta."""
    project_root = Path.cwd().resolve() if current_path is None else Path(current_path).resolve()
    if project_root.name == "notebooks":
        project_root = project_root.parent

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    return project_root


def get_bai_columns(df: pd.DataFrame) -> list[str]:
    """Retorna columnas BAI ordenadas por numero de item."""
    return sorted(
        [column for column in df.columns if column.startswith("BAI_")],
        key=lambda column: int(column.split("_")[1]),
    )


def validate_bai_analysis_columns(
    df: pd.DataFrame,
    bai_columns: list[str] | None = None,
    expected_items: int = 21,
    required_columns: tuple[str, ...] = ("category", "totalScore"),
) -> list[str]:
    """Valida columnas base para notebooks de analisis y retorna columnas BAI."""
    bai_columns = get_bai_columns(df) if bai_columns is None else bai_columns
    missing_columns = sorted(set(required_columns).difference(df.columns))

    if missing_columns:
        raise ValueError(f"Faltan columnas esperadas: {missing_columns}")

    if len(bai_columns) != expected_items:
        raise ValueError(
            f"Se esperaban {expected_items} sintomas BAI, pero se encontraron {len(bai_columns)}"
        )

    score_matches_items = df[bai_columns].sum(axis=1).eq(df["totalScore"])
    if not score_matches_items.all():
        raise ValueError("Hay filas donde totalScore no coincide con la suma de BAI_1..BAI_21")

    return bai_columns


def build_dataset_summary(df: pd.DataFrame, bai_columns: list[str]) -> pd.DataFrame:
    """Construye resumen compacto del dataset procesado."""
    return pd.DataFrame({
        "filas": [len(df)],
        "columnas": [df.shape[1]],
        "síntomas_BAI": [len(bai_columns)],
        "score_min": [df["totalScore"].min()],
        "score_mediana": [df["totalScore"].median()],
        "score_max": [df["totalScore"].max()],
    })


def build_symptom_correlation_table(
    df: pd.DataFrame,
    score_column: str = "totalScore",
    bai_columns: list[str] | None = None,
    include_labels: bool = True,
) -> pd.DataFrame:
    """Calcula la correlación de cada síntoma BAI contra el score total."""
    bai_columns = get_bai_columns(df) if bai_columns is None else bai_columns
    validate_bai_analysis_columns(df, bai_columns, required_columns=(score_column,))

    corr_series = (
        df[bai_columns + [score_column]]
        .corr(numeric_only=True)[score_column]
        .drop(score_column)
        .sort_values(ascending=False)
    )

    corr_df = corr_series.rename_axis("symptom").reset_index(name="correlation")
    if include_labels:
        corr_df["label"] = corr_df["symptom"].map(BAI_SYMPTOMS)

    return corr_df


def export_symptom_correlations(
    df: pd.DataFrame,
    output_path: str | Path,
    score_column: str = "totalScore",
    bai_columns: list[str] | None = None,
    include_labels: bool = False,
) -> Path:
    """Exporta a CSV la correlación de síntomas BAI contra el score total."""
    correlation_table = build_symptom_correlation_table(
        df,
        score_column=score_column,
        bai_columns=bai_columns,
        include_labels=include_labels,
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    correlation_table.to_csv(output_path, index=False)
    return output_path


def build_category_counts(df: pd.DataFrame, category_order: list[str] | None = None) -> pd.DataFrame:
    """Cuenta categorias y calcula porcentajes."""
    category_order = CATEGORY_ORDER if category_order is None else category_order
    category_counts = (
        df["category"]
        .value_counts()
        .reindex(category_order, fill_value=0)
        .rename_axis("category")
        .reset_index(name="count")
    )
    category_counts["percentage"] = category_counts["count"] / category_counts["count"].sum() * 100
    return category_counts


def bai_label_map(bai_columns: list[str], short: bool = False, include_code: bool = True) -> dict[str, str]:
    """Crea etiquetas para columnas BAI."""
    symptom_map = BAI_SHORT_SYMPTOMS if short else BAI_SYMPTOMS

    if short:
        return {column: f"{column.split('_')[1]}. {symptom_map[column]}" for column in bai_columns}

    if include_code:
        return {column: f"{column}: {symptom_map[column]}" for column in bai_columns}

    return {column: symptom_map[column] for column in bai_columns}


def wrap_label(label: object, width: int = 22) -> str:
    """Envuelve una etiqueta larga para graficos."""
    return "\n".join(wrap(str(label), width=width, break_long_words=False))


def polish_axes(ax, grid_axis: str = "y"):
    """Aplica estilo visual comun a ejes matplotlib."""
    import seaborn as sns

    ax.grid(axis=grid_axis, color="#E6E6E6", linewidth=1)
    if grid_axis == "y":
        ax.grid(axis="x", visible=False)
    elif grid_axis == "x":
        ax.grid(axis="y", visible=False)
    sns.despine(ax=ax, left=True, bottom=False)
    ax.title.set_color("#222222")
    ax.tick_params(axis="both", pad=7)
    return ax


def save_plot(fig, filename: str, output_dir: str | Path, dpi: int = 220) -> Path:
    """Guarda una figura y retorna su ruta."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    fig.tight_layout()
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight", facecolor="white")
    return output_path


def evaluate_kmeans_range(
    X_scaled,
    k_values=range(2, 7),
    random_state: int = 42,
    n_init: int = 50,
) -> pd.DataFrame:
    """Evalua inertia y silhouette para varios valores de k."""
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score

    k_results = []
    for k in k_values:
        model = KMeans(n_clusters=k, random_state=random_state, n_init=n_init)
        labels = model.fit_predict(X_scaled)
        k_results.append({
            "k": k,
            "inertia": model.inertia_,
            "silhouette": silhouette_score(X_scaled, labels),
        })

    return pd.DataFrame(k_results)


def assign_ordered_clusters(
    df: pd.DataFrame,
    raw_cluster_column: str = "cluster_raw",
    score_column: str = "totalScore",
    cluster_column: str = "cluster",
) -> pd.DataFrame:
    """Ordena clusters por score promedio y agrega una columna categorica legible."""
    clustered_df = df.copy()
    cluster_order = (
        clustered_df.groupby(raw_cluster_column)[score_column]
        .mean()
        .sort_values()
        .index
        .tolist()
    )
    cluster_name_map = {
        raw: f"Cluster {rank + 1}"
        for rank, raw in enumerate(cluster_order)
    }
    clustered_df[cluster_column] = pd.Categorical(
        clustered_df[raw_cluster_column].map(cluster_name_map),
        categories=[f"Cluster {idx}" for idx in range(1, len(cluster_order) + 1)],
        ordered=True,
    )
    return clustered_df


def summarize_clusters(
    df: pd.DataFrame,
    cluster_column: str = "cluster",
    id_column: str = "id",
    score_column: str = "totalScore",
) -> pd.DataFrame:
    """Resume tamano y scores por cluster."""
    cluster_summary = (
        df.groupby(cluster_column, observed=True)
        .agg(
            n=(id_column, "count"),
            score_promedio=(score_column, "mean"),
            score_mediana=(score_column, "median"),
            score_min=(score_column, "min"),
            score_max=(score_column, "max"),
        )
        .round(2)
    )
    cluster_summary["porcentaje"] = (cluster_summary["n"] / len(df) * 100).round(1)
    return cluster_summary
