import random
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "dataset"
SRC_IMAGE_DIR = DATASET_DIR / "image"
SRC_JSON_DIR = DATASET_DIR / "json"
SPLITS = {
    "train": 0.8,
    "val": 0.1,
    "test": 0.1,
}
SEED = 20260425


def clear_split_dirs() -> None:
    for split in SPLITS:
        split_dir = DATASET_DIR / split
        if split_dir.exists():
            shutil.rmtree(split_dir)
        (split_dir / "image").mkdir(parents=True, exist_ok=True)
        (split_dir / "json").mkdir(parents=True, exist_ok=True)


def load_pairs() -> list[tuple[Path, Path]]:
    pairs = []
    for image_path in sorted(SRC_IMAGE_DIR.glob("*.jpg")):
        json_path = SRC_JSON_DIR / f"{image_path.stem}.json"
        if json_path.exists():
            pairs.append((image_path, json_path))
    return pairs


def split_pairs(pairs: list[tuple[Path, Path]]) -> dict[str, list[tuple[Path, Path]]]:
    shuffled = pairs[:]
    random.Random(SEED).shuffle(shuffled)

    total = len(shuffled)
    train_count = int(total * SPLITS["train"])
    val_count = int(total * SPLITS["val"])
    test_count = total - train_count - val_count

    return {
        "train": shuffled[:train_count],
        "val": shuffled[train_count:train_count + val_count],
        "test": shuffled[train_count + val_count:train_count + val_count + test_count],
    }


def copy_split(split_name: str, items: list[tuple[Path, Path]]) -> None:
    image_dir = DATASET_DIR / split_name / "image"
    json_dir = DATASET_DIR / split_name / "json"
    for image_path, json_path in items:
        shutil.copy2(image_path, image_dir / image_path.name)
        shutil.copy2(json_path, json_dir / json_path.name)


def main() -> None:
    pairs = load_pairs()
    clear_split_dirs()
    split_map = split_pairs(pairs)
    for split_name, items in split_map.items():
        copy_split(split_name, items)
        print(split_name, len(items))


if __name__ == "__main__":
    main()
