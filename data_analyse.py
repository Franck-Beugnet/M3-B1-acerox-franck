import os
from pathlib import Path

import pandas as pd


def print_section(title: str) -> None:
    print("\n" + "=" * 5 + f" {title} " + "=" * 5)


def load_sources(base_dir: Path) -> dict[str, pd.DataFrame]:
    files = {
        "capteurs_iot": "capteurs_iot.csv",
        "erp": "erp_export.json",
        "logs": "logs_machines.log",
    }

    capteurs = pd.read_csv(base_dir / files["capteurs_iot"])
    erp = pd.read_json(base_dir / files["erp"])
    # Chargement brut du log en une seule colonne texte.
    logs = pd.read_table(base_dir / files["logs"], header=None, names=["raw_log"])

    return {
        "files": files,
        "capteurs_iot": capteurs,
        "erp": erp,
        "logs": logs,
    }


def print_profile(name: str, df: pd.DataFrame) -> None:
    print_section(name.upper())
    print(f"shape={df.shape}")
    print("info:")
    df.info()

    print("\nhead:")
    print(df.head(5).to_string(index=False))

    print("\ndescribe(include='all') (first columns):")
    desc = df.describe(include="all").transpose()
    print(desc.head(10).to_string())


def print_volumes(base_dir: Path, files: dict[str, str]) -> None:
    print_section("VOLUME")
    for name, filename in files.items():
        path = base_dir / filename
        print(name, filename, "size_bytes=", os.path.getsize(path))


def print_quality_checks(capteurs: pd.DataFrame, erp: pd.DataFrame, logs: pd.DataFrame) -> None:
    print_section("QUALITY CHECKS")

    print("capteurs nulls by column:")
    print(capteurs.isna().sum().to_string())
    print("capteurs outlier temperature >120:", int((capteurs["temperature_c"] > 120).sum()))
    print("capteurs vibration == 12.0:", int((capteurs["vibration_mms"] == 12.0).sum()))

    print("\nerp nulls by column:")
    print(erp.isna().sum().to_string())
    print("erp duplicate ordre_id:", int(erp["ordre_id"].duplicated().sum()))
    print(
        "erp date_fin_prevue < date_lancement:",
        int(
            (
                pd.to_datetime(erp["date_fin_prevue"])
                < pd.to_datetime(erp["date_lancement"])
            ).sum()
        ),
    )

    print("\nlogs nulls by column:")
    print(logs.isna().sum().to_string())
    print("logs duplicated raw_log:", int(logs["raw_log"].duplicated().sum()))


def main() -> None:
    base_dir = Path("data")
    sources = load_sources(base_dir)

    print_profile("capteurs_iot", sources["capteurs_iot"])
    print_profile("erp", sources["erp"])
    print_profile("logs", sources["logs"])

    print_volumes(base_dir, sources["files"])
    print_quality_checks(sources["capteurs_iot"], sources["erp"], sources["logs"])


if __name__ == "__main__":
    main()
