import json
import random
import shutil
from pathlib import Path
from typing import Any

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = ROOT / "dataset"
DST_ROOT = ROOT / "dataset_augmented"
SPLITS = ("train", "val", "test")
IMAGE_SIZE = 640
RANDOM_SEED = 20260425


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def ensure_clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def load_records(split: str) -> list[dict[str, Any]]:
    image_dir = SRC_ROOT / split / "image"
    json_dir = SRC_ROOT / split / "json"
    records = []

    for image_path in sorted(image_dir.glob("*.jpg")):
        json_path = json_dir / f"{image_path.stem}.json"
        if not json_path.exists():
            continue
        image = cv2.imread(str(image_path))
        if image is None:
            continue
        ann = read_json(json_path)
        records.append(
            {
                "stem": image_path.stem,
                "image_path": image_path,
                "json_path": json_path,
                "image": image,
                "ann": ann,
            }
        )

    return records


def adjust_brightness(image: np.ndarray, factor: float) -> np.ndarray:
    out = np.clip(image.astype(np.float32) * factor, 0, 255)
    return out.astype(np.uint8)


def add_noise(image: np.ndarray, sigma: float) -> np.ndarray:
    noise = np.random.normal(0.0, sigma, image.shape).astype(np.float32)
    out = np.clip(image.astype(np.float32) + noise, 0, 255)
    return out.astype(np.uint8)


def transform_points(points: list[list[float]], matrix: np.ndarray) -> list[list[float]]:
    transformed = []
    for x, y in points:
        nx = float(matrix[0, 0] * x + matrix[0, 1] * y + matrix[0, 2])
        ny = float(matrix[1, 0] * x + matrix[1, 1] * y + matrix[1, 2])
        transformed.append([nx, ny])
    return transformed


def points_inside_image(points: list[list[float]]) -> bool:
    return all(0.0 <= x < IMAGE_SIZE and 0.0 <= y < IMAGE_SIZE for x, y in points)


def scale_annotation(ann: dict[str, Any], scale: float) -> dict[str, Any]:
    center = IMAGE_SIZE / 2.0
    tx = center - scale * center
    ty = center - scale * center
    matrix = np.array(
        [
            [scale, 0.0, tx],
            [0.0, scale, ty],
        ],
        dtype=np.float32,
    )

    new_shapes = []
    for shape in ann.get("shapes", []):
        new_shape = dict(shape)
        new_points = transform_points(shape.get("points", []), matrix)
        if not points_inside_image(new_points):
            continue
        new_shape["points"] = new_points
        new_shapes.append(new_shape)

    result = dict(ann)
    result["shapes"] = new_shapes
    return result


def scale_image(image: np.ndarray, scale: float) -> np.ndarray:
    matrix = np.array(
        [
            [scale, 0.0, IMAGE_SIZE / 2.0 - scale * IMAGE_SIZE / 2.0],
            [0.0, scale, IMAGE_SIZE / 2.0 - scale * IMAGE_SIZE / 2.0],
        ],
        dtype=np.float32,
    )
    return cv2.warpAffine(
        image,
        matrix,
        (IMAGE_SIZE, IMAGE_SIZE),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT_101,
    )


def remap_shape_points(shape: dict[str, Any], scale: float, offset_x: int, offset_y: int) -> dict[str, Any]:
    new_shape = dict(shape)
    new_shape["points"] = [
        [float(x) * scale + offset_x, float(y) * scale + offset_y]
        for x, y in shape.get("points", [])
    ]
    return new_shape


def build_mosaic(records: list[dict[str, Any]], start_idx: int) -> tuple[np.ndarray, dict[str, Any], str]:
    chosen = [records[(start_idx + i) % len(records)] for i in range(4)]
    canvas = np.zeros((IMAGE_SIZE, IMAGE_SIZE, 3), dtype=np.uint8)
    placements = [
        (0, 0),
        (320, 0),
        (0, 320),
        (320, 320),
    ]
    all_shapes = []
    name_parts = []

    for record, (ox, oy) in zip(chosen, placements):
        resized = cv2.resize(record["image"], (320, 320), interpolation=cv2.INTER_LINEAR)
        canvas[oy:oy + 320, ox:ox + 320] = resized
        for shape in record["ann"].get("shapes", []):
            all_shapes.append(remap_shape_points(shape, 0.5, ox, oy))
        name_parts.append(record["stem"])

    ann = {
        "version": chosen[0]["ann"].get("version", "3.0.3"),
        "flags": {},
        "shapes": all_shapes,
        "imagePath": "",
        "imageData": None,
        "imageHeight": IMAGE_SIZE,
        "imageWidth": IMAGE_SIZE,
        "description": "mosaic augmentation",
    }
    return canvas, ann, "__".join(name_parts)


def save_sample(split: str, name: str, image: np.ndarray, ann: dict[str, Any], note: str) -> None:
    image_dir = DST_ROOT / split / "image"
    json_dir = DST_ROOT / split / "json"
    image_name = f"{name}.jpg"
    json_name = f"{name}.json"

    cv2.imwrite(str(image_dir / image_name), image)

    sample_ann = dict(ann)
    sample_ann["imagePath"] = image_name
    sample_ann["imageWidth"] = IMAGE_SIZE
    sample_ann["imageHeight"] = IMAGE_SIZE
    sample_ann["imageData"] = None
    sample_ann["description"] = note
    write_json(json_dir / json_name, sample_ann)


def copy_originals(split: str, records: list[dict[str, Any]]) -> None:
    image_dir = DST_ROOT / split / "image"
    json_dir = DST_ROOT / split / "json"
    for record in records:
        shutil.copy2(record["image_path"], image_dir / record["image_path"].name)
        shutil.copy2(record["json_path"], json_dir / record["json_path"].name)


def prepare_split_dirs() -> None:
    ensure_clean_dir(DST_ROOT)
    for split in SPLITS:
        (DST_ROOT / split / "image").mkdir(parents=True, exist_ok=True)
        (DST_ROOT / split / "json").mkdir(parents=True, exist_ok=True)


def augment_split(split: str) -> dict[str, int]:
    records = load_records(split)
    copy_originals(split, records)

    for record in records:
        stem = record["stem"]
        image = record["image"]
        ann = record["ann"]

        save_sample(split, f"{stem}_aug_bright", adjust_brightness(image, 1.20), ann, "brightness up")
        save_sample(split, f"{stem}_aug_dark", adjust_brightness(image, 0.80), ann, "brightness down")

        scaled_image = scale_image(image, 1.05)
        scaled_ann = scale_annotation(ann, 1.05)
        save_sample(split, f"{stem}_aug_scale", scaled_image, scaled_ann, "slight scale")

        save_sample(split, f"{stem}_aug_noise", add_noise(image, 10.0), ann, "gaussian noise")

    for idx in range(len(records)):
        mosaic_image, mosaic_ann, mosaic_key = build_mosaic(records, idx)
        save_sample(split, f"mosaic_{idx:04d}_{mosaic_key}", mosaic_image, mosaic_ann, "mosaic")

    return {
        "originals": len(records),
        "bright": len(records),
        "dark": len(records),
        "scale": len(records),
        "noise": len(records),
        "mosaic": len(records),
        "total": len(records) * 6,
    }


def main() -> None:
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    prepare_split_dirs()

    for split in SPLITS:
        stats = augment_split(split)
        print(
            f"{split}: originals={stats['originals']}, bright={stats['bright']}, "
            f"dark={stats['dark']}, scale={stats['scale']}, noise={stats['noise']}, "
            f"mosaic={stats['mosaic']}, total={stats['total']}"
        )


if __name__ == "__main__":
    main()
