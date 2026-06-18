### Frappe Chinese Language Pack

A custom app to integrate optimized Chinese language translations for Frappe apps.

### How it works

This app keeps translations separated by upstream Frappe app instead of merging all
messages into one global `zh.po`.

Translation sources live under app-specific folders:

```text
frappe_translation/locale/frappe/zh.po
frappe_translation/locale/erpnext/zh.po
frappe_translation/locale/hrms/zh.po
frappe_translation/locale/crm/zh.po
frappe_translation/locale/insights/zh.po
frappe_translation/locale/education/zh.csv
```

On install and migrate, the pack compiles those bundled sources into Frappe's runtime
catalogs using the target app name as the gettext domain:

```text
sites/assets/locale/zh/LC_MESSAGES/frappe.mo
sites/assets/locale/zh/LC_MESSAGES/erpnext.mo
sites/assets/locale/zh/LC_MESSAGES/hrms.mo
```

That means the same `msgid` can have a different translation in each app source file.
The old generated `frappe_translation/locale/zh.po` file is intentionally not used,
because it collapses app-specific meaning into one global dictionary.

If the original app code uses the same text without a translation context, Frappe still
looks up the plain `msgid`. For truly different meanings in the same runtime page,
prefer upstream strings with context, for example:

```python
_("Open", context="Sales Invoice status")
```

```javascript
__("Open", null, "Job Opening status")
```

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch main
bench install-app frappe_translation
```

To recompile the bundled translations after editing the source files:

```bash
bench --site $SITE_NAME execute frappe_translation.translation_pack.install_translation_pack
bench --site $SITE_NAME clear-cache
```

To audit app-specific conflicts without merging them:

```bash
python frappe_translation/scripts/audit_zh_sources.py
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/frappe_translation
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade
### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

gpl-3.0
"# frappe_translation" 
