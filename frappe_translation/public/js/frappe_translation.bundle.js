// Frappe Translation app bundle
// Verifies that static JS assets are loaded and accessible from the frontend.

window.frappe_translation = {
	version: "0.0.14",

	assets: {
		css: "frappe_translation.bundle.css",
		js: "frappe_translation.bundle.js",
		logo: "/assets/frappe_translation/logo.png",
	},

	checkAssets() {
		const results = { css: false, js: true, logo: false };

		// CSS is loaded via app_include_css; verify a known rule is applied.
		const probe = document.createElement("div");
		probe.className = "frappe-translation-page";
		probe.style.position = "absolute";
		probe.style.left = "-9999px";
		document.body.appendChild(probe);
		const style = window.getComputedStyle(probe);
		results.css = style.maxWidth === "960px";
		document.body.removeChild(probe);

		// Logo is reachable via a fetch.
		fetch(this.assets.logo, { method: "HEAD" })
			.then((resp) => {
				results.logo = resp.ok;
				this.renderStatus(results);
			})
			.catch(() => this.renderStatus(results));

		return results;
	},

	renderStatus(results) {
		const container = document.querySelector("[data-asset-status]");
		if (!container) return;
		container.innerHTML = "";
		for (const [name, ok] of Object.entries(results)) {
			const badge = document.createElement("span");
			badge.className = "status-badge" + (ok ? "" : " error");
			badge.textContent = `${name}: ${ok ? "loaded" : "missing"}`;
			container.appendChild(badge);
			container.appendChild(document.createTextNode(" "));
		}
	},

	init() {
		if (document.readyState === "loading") {
			document.addEventListener("DOMContentLoaded", () => this.checkAssets());
		} else {
			this.checkAssets();
		}
	},
};

window.frappe_translation.init();
