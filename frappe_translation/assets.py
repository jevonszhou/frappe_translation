from __future__ import annotations

import shutil
from pathlib import Path

APP_NAME = "frappe_translation"
PUBLIC_DIR = "public"


def ensure_static_assets() -> str:
	"""Ensure /assets/frappe_translation contains this app's public assets.

	Frappe's normal asset linker often creates symlinks. In Docker deployments, the
	frontend container may serve sites/assets without mounting apps/, so a symlink to
	apps/frappe_translation/public can look valid in backend but return 404 in nginx.
	Use a real copied directory to keep the assets visible to every container that
	shares the sites volume.
	"""
	source_dir = get_public_dir()
	target_dir = get_assets_dir() / APP_NAME

	if not source_dir.exists():
		raise FileNotFoundError(f"Missing static assets source directory: {source_dir}")

	target_dir.parent.mkdir(parents=True, exist_ok=True)

	if target_dir.is_symlink():
		target_dir.unlink()

	if target_dir.exists():
		if not target_dir.is_dir():
			raise FileExistsError(f"Static assets target exists and is not a directory: {target_dir}")
		copy_public_assets(source_dir, target_dir)
		return str(target_dir)

	copy_public_assets(source_dir, target_dir)
	return str(target_dir)


def copy_public_assets(source_dir: Path, target_dir: Path) -> None:
	shutil.copytree(
		source_dir,
		target_dir,
		dirs_exist_ok=True,
		ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
	)


def get_public_dir() -> Path:
	import frappe

	return Path(frappe.get_app_path(APP_NAME, PUBLIC_DIR))


def get_assets_dir() -> Path:
	from frappe.utils import get_bench_path

	return Path(get_bench_path()) / "sites" / "assets"
