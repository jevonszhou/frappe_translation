from frappe_translation.assets import ensure_static_assets
from frappe_translation.translation_pack import install_translation_pack


def sync_translation_app():
	ensure_static_assets()
	install_translation_pack()


def after_install():
	sync_translation_app()


def after_migrate():
	sync_translation_app()


def after_build():
	sync_translation_app()
