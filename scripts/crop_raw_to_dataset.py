import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RAW_IMAGES = ROOT / "raw" / "images"
RAW_JSON = ROOT / "raw" / "json"
DATASET_IMAGES = ROOT / "dataset" / "image"
DATASET_JSON = ROOT / "dataset" / "json"

CROP_SIZE = 640


def point_in_crop(x: float, y: float, crop_x: int, crop_y: int) -> bool:
    return crop_x <= x < crop_x + CROP_SIZE and crop_y <= y < crop_y + CROP_SIZE


def shape_in_crop(shape: dict[str, Any], crop_x: int, crop_y: int) -> bool:
    points = shape.get("points", [])
    if not points:
        return False
    return all(point_in_crop(float(x), float(y), crop_x, crop_y) for x, y in points)


def remap_shape(shape: dict[str, Any], crop_x: int, crop_y: int) -> dict[str, Any]:
    cloned = dict(shape)
    cloned["points"] = [
        [float(x) - crop_x, float(y) - crop_y]
        for x, y in shape.get("points", [])
    ]
    return cloned


def is_point_shape(shape: dict[str, Any]) -> bool:
    return shape.get("shape_type") == "point" and len(shape.get("points", [])) == 1


def is_rotation_shape(shape: dict[str, Any]) -> bool:
    return shape.get("shape_type") == "rotation" and len(shape.get("points", [])) == 4


def point_inside_rotation_box(point_shape: dict[str, Any], rotation_shape: dict[str, Any]) -> bool:
    px, py = point_shape["points"][0]
    contour = [
        [float(x), float(y)]
        for x, y in rotation_shape["points"]
    ]
    return cv2.pointPolygonTest(
        np.array(contour, dtype="float32"),
        (float(px), float(py)),
        False,
    ) >= 0


def clip_rotation_shape(
    shape: dict[str, Any],
    crop_x: int,
    crop_y: int,
    crop_points: list[dict[str, Any]],
) -> dict[str, Any] | None:
    rect_points = [
        [float(x), float(y)]
        for x, y in shape["points"]
    ]

    inside_flags = [
        point_in_crop(x, y, crop_x, crop_y)
        for x, y in rect_points
    ]
    fully_inside = all(inside_flags)
    partially_inside = any(inside_flags) and not fully_inside

    if fully_inside:
        return remap_shape(shape, crop_x, crop_y)

    if not partially_inside:
        return None

    has_point = any(
        point_inside_rotation_box(point_shape, shape)
        for point_shape in crop_points
    )
    if not has_point:
        return None

    crop_rect = (
        (crop_x + CROP_SIZE / 2.0, crop_y + CROP_SIZE / 2.0),
        (float(CROP_SIZE), float(CROP_SIZE)),
        0.0,
    )
    rotation_rect = cv2.minAreaRect(
        np.array(rect_points, dtype="float32")
    )
    intersect_type, intersect_pts = cv2.rotatedRectangleIntersection(crop_rect, rotation_rect)
    if intersect_type == cv2.INTERSECT_NONE or intersect_pts is None or len(intersect_pts) < 3:
        return None

    clipped_rect = cv2.minAreaRect(intersect_pts)
    clipped_box = cv2.boxPoints(clipped_rect)

    cloned = dict(shape)
    cloned["points"] = [
        [float(x) - crop_x, float(y) - crop_y]
        for x, y in clipped_box.tolist()
    ]
    return cloned


def build_crop_json(source: dict[str, Any], crop_name: str, crop_x: int, crop_y: int) -> dict[str, Any]:
    point_shapes = [
        remap_shape(shape, crop_x, crop_y)
        for shape in source.get("shapes", [])
        if is_point_shape(shape) and shape_in_crop(shape, crop_x, crop_y)
    ]

    other_shapes = []
    for shape in source.get("shapes", []):
        if is_point_shape(shape):
            continue
        if is_rotation_shape(shape):
            clipped = clip_rotation_shape(shape, crop_x, crop_y, point_shapes)
            if clipped is not None:
                other_shapes.append(clipped)
            continue
        if shape_in_crop(shape, crop_x, crop_y):
            other_shapes.append(remap_shape(shape, crop_x, crop_y))

    result = dict(source)
    result["shapes"] = point_shapes + other_shapes
    result["imagePath"] = crop_name
    result["imageData"] = None
    result["imageHeight"] = CROP_SIZE
    result["imageWidth"] = CROP_SIZE
    return result


def process_file(image_path: Path) -> None:
    json_path = RAW_JSON / f"{image_path.stem}.json"
    if not json_path.exists():
        return

    image = Image.open(image_path)
    width, height = image.size
    if width < CROP_SIZE or height < CROP_SIZE:
        return

    crop_y = max((height - CROP_SIZE) // 2, 0)
    crop_specs = [
        ("left", 0, crop_y),
        ("right", width - CROP_SIZE, crop_y),
    ]

    with json_path.open("r", encoding="utf-8") as f:
        source = json.load(f)

    for suffix, crop_x, crop_y in crop_specs:
        crop = image.crop((crop_x, crop_y, crop_x + CROP_SIZE, crop_y + CROP_SIZE))
        crop_name = f"{image_path.stem}_{suffix}.jpg"
        out_image = DATASET_IMAGES / crop_name
        out_json = DATASET_JSON / f"{image_path.stem}_{suffix}.json"

        crop.save(out_image, quality=95)
        crop_json = build_crop_json(source, crop_name, crop_x, crop_y)
        with out_json.open("w", encoding="utf-8") as f:
            json.dump(crop_json, f, ensure_ascii=False, indent=2)


def main() -> None:
    DATASET_IMAGES.mkdir(parents=True, exist_ok=True)
    DATASET_JSON.mkdir(parents=True, exist_ok=True)

    for path in DATASET_IMAGES.glob("*.jpg"):
        path.unlink()
    for path in DATASET_JSON.glob("*.json"):
        path.unlink()

    for image_path in sorted(RAW_IMAGES.glob("*.jpg")):
        process_file(image_path)


if __name__ == "__main__":
    main()
