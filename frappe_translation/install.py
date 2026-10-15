from frappe_translation.assets import ensure_static_assets
from frappe_translation.translation_pack import install_translation_pack


def sync_translation_app():
	ensure_static_assets()
	install_translation_pack()


def after_install():
	sync_translation_app()


def after_migrate():
	sync_translation_app()
	remove_legacy_desktop_icon()


def after_build():
	sync_translation_app()


def remove_legacy_desktop_icon():
	"""Remove this app's obsolete Desktop Icon when upgrading an existing site."""
	import frappe

	if not frappe.db.table_exists("Desktop Icon"):
		return

	icon_names = frappe.get_all(
		"Desktop Icon",
		filters={"icon_type": "App", "app": "frappe_translation"},
		pluck="name",
	)
	for icon_name in icon_names:
		frappe.delete_doc("Desktop Icon", icon_name, ignore_permissions=True, force=True)
