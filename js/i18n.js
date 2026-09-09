(() => {
    const supportedLanguages = ["es", "en", "uk", "ru", "ro"];
    const defaultLanguage = "es";

    let currentLanguage = defaultLanguage;
    let currentTranslations = null;

    function setText(id, value) {
        if (value === undefined || value === null) return;

        document.querySelectorAll(`[id="${id}"]`).forEach((element) => {
            element.textContent = value;
        });
    }

    function applyTranslations(data, lang) {
        document.documentElement.lang = lang;
        document.title = data.title;

        setText("nav_home", data.menu.home);
        setText("nav_about", data.menu.about);
        setText("nav_services", data.menu.services);
        setText("nav_contact_btn", data.menu.contact);
        setText("nav_language", data.menu.language);

        setText("offcanvas_schedule", data.offcanvas.schedule);
        setText("offcanvas_phone", data.offcanvas.phone);
        setText("header_schedule", data.header.schedule);
        setText("header_phone", data.header.phone);

        setText("hero_subtitle", data.hero.subtitle);
        setText("hero_title", data.hero.title);
        setText("hero_contact_btn", data.hero.contact_btn);

        setText("about_subtitle", data.about.subtitle);
        setText("about_title", data.about.title);
        setText("about_description", data.about.description);
        setText("feature_1_title", data.about.feature_1_title);
        setText("feature_1_description", data.about.feature_1_description);
        setText("feature_2_title", data.about.feature_2_title);
        setText("feature_2_description", data.about.feature_2_description);
        setText("feature_3_title", data.about.feature_3_title);
        setText("feature_3_description", data.about.feature_3_description);

        setText("feature_subtitle", data.features.subtitle);
        setText("feature_title", data.features.title);
        setText("feature_description_1", data.features.description_1);
        setText("feature_description_2", data.features.description_2);
        setText("feature_about_btn", data.features.about_btn);
        for (let i = 1; i <= 6; i += 1) {
            setText(`feature_item_${i}`, data.features[`item_${i}`]);
        }

        setText("contact_title", data.contact.title);
        setText("work_with_us_title", data.contact.work_with_us_title);
        setText("contact_info_text", data.contact.info_text);
        setText("contact_phone_label", data.contact.phone_label);
        setText("contact_email_label", data.contact.email_label);
        setText("work_hours_label", data.contact.work_hours_label);
        setText("saturday_label", data.contact.saturday_label);

        setText("services_title", data.services.title);
        for (let i = 1; i <= 10; i += 1) {
            setText(`service_${i}`, data.services[`service_${i}`]);
        }

        setText("clients_title", data.clients.title);

        setText("footer_contact_title", data.footer.contact_title);
        setText("footer_phone", data.footer.phone);
        setText("footer_email", data.footer.email);
        setText("footer_address", data.footer.address);
        setText("footer_links_title", data.footer.links_title);
        setText("footer_link_home", data.footer.link_home);
        setText("footer_link_about", data.footer.link_about);
        setText("footer_link_services", data.footer.link_services);
        setText("footer_link_contact", data.footer.link_contact);
        setText("footer_copyright", data.footer.copyright);

        setText("callback_title", data.callback.title);
        setText("callback_description", data.callback.description);
        setText("callback_submit", data.callback.submit);

        const nameInput = document.getElementById("callback_name");
        const phoneInput = document.getElementById("callback_phone_input");
        if (nameInput) nameInput.placeholder = data.callback.name_placeholder;
        if (phoneInput) phoneInput.placeholder = data.callback.phone_placeholder;
    }

    async function setLanguage(lang) {
        const language = supportedLanguages.includes(lang) ? lang : defaultLanguage;

        try {
            const response = await fetch(`lang/${language}.json`, { cache: "no-cache" });
            if (!response.ok) {
                throw new Error(`Could not load lang/${language}.json (${response.status})`);
            }

            const data = await response.json();
            currentLanguage = language;
            currentTranslations = data;
            applyTranslations(data, language);
            localStorage.setItem("temploMotorLanguage", language);

            document.dispatchEvent(new CustomEvent("templo:language-changed", {
                detail: { lang: language, translations: data }
            }));
        } catch (error) {
            console.error("Language loading error:", error);
        }
    }

    document.addEventListener("click", (event) => {
        const languageLink = event.target.closest("[data-lang]");
        if (!languageLink) return;

        event.preventDefault();
        setLanguage(languageLink.dataset.lang);
    });

    document.addEventListener("DOMContentLoaded", () => {
        const savedLanguage = localStorage.getItem("temploMotorLanguage");
        setLanguage(savedLanguage || defaultLanguage);
    });

    window.setLanguage = setLanguage;
    window.TemploI18n = {
        setLanguage,
        getCurrentLanguage: () => currentLanguage,
        getTranslations: () => currentTranslations
    };
})();
