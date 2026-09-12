from pathlib import Path
import json
import re
import html

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "src" / "index.template.html"
LANG_DIR = ROOT / "lang"

BASE_URL = "https://templo-motor.com"

LANGUAGES = {
    "es": {
        "file": "es.json",
        "output": ROOT / "index.html",
        "url": "/"
    },
    "en": {
        "file": "en.json",
        "output": ROOT / "en" / "index.html",
        "url": "/en/"
    },
    "uk": {
        "file": "uk.json",
        "output": ROOT / "uk" / "index.html",
        "url": "/uk/"
    },
    "ru": {
        "file": "ru.json",
        "output": ROOT / "ru" / "index.html",
        "url": "/ru/"
    },
    "ro": {
        "file": "ro.json",
        "output": ROOT / "ro" / "index.html",
        "url": "/ro/"
    }
}

TEXT_MAP = {
    "nav_home": ("menu", "home"),
    "nav_about": ("menu", "about"),
    "nav_services": ("menu", "services"),
    "nav_contact_btn": ("menu", "contact"),
    "nav_language": ("menu", "language"),

    "offcanvas_schedule": ("offcanvas", "schedule"),
    "offcanvas_phone": ("offcanvas", "phone"),
    "header_schedule": ("header", "schedule"),
    "header_phone": ("header", "phone"),

    "hero_subtitle": ("hero", "subtitle"),
    "hero_title": ("hero", "title"),
    "hero_contact_btn": ("hero", "contact_btn"),

    "about_subtitle": ("about", "subtitle"),
    "about_title": ("about", "title"),
    "about_description": ("about", "description"),
    "feature_1_title": ("about", "feature_1_title"),
    "feature_1_description": ("about", "feature_1_description"),
    "feature_2_title": ("about", "feature_2_title"),
    "feature_2_description": ("about", "feature_2_description"),
    "feature_3_title": ("about", "feature_3_title"),
    "feature_3_description": ("about", "feature_3_description"),

    "feature_subtitle": ("features", "subtitle"),
    "feature_title": ("features", "title"),
    "feature_description_1": ("features", "description_1"),
    "feature_description_2": ("features", "description_2"),
    "feature_about_btn": ("features", "about_btn"),
    "feature_item_1": ("features", "item_1"),
    "feature_item_2": ("features", "item_2"),
    "feature_item_3": ("features", "item_3"),
    "feature_item_4": ("features", "item_4"),
    "feature_item_5": ("features", "item_5"),
    "feature_item_6": ("features", "item_6"),

    "contact_title": ("contact", "title"),
    "work_with_us_title": ("contact", "work_with_us_title"),
    "contact_info_text": ("contact", "info_text"),
    "contact_phone_label": ("contact", "phone_label"),
    "contact_email_label": ("contact", "email_label"),
    "work_hours_label": ("contact", "work_hours_label"),
    "saturday_label": ("contact", "saturday_label"),

    "services_title": ("services", "title"),
    "service_1": ("services", "service_1"),
    "service_2": ("services", "service_2"),
    "service_3": ("services", "service_3"),
    "service_4": ("services", "service_4"),
    "service_5": ("services", "service_5"),
    "service_6": ("services", "service_6"),
    "service_7": ("services", "service_7"),
    "service_8": ("services", "service_8"),
    "service_9": ("services", "service_9"),
    "service_10": ("services", "service_10"),

    "clients_title": ("clients", "title"),

    "footer_contact_title": ("footer", "contact_title"),
    "footer_phone": ("footer", "phone"),
    "footer_email": ("footer", "email"),
    "footer_address": ("footer", "address"),
    "footer_links_title": ("footer", "links_title"),
    "footer_link_home": ("footer", "link_home"),
    "footer_link_about": ("footer", "link_about"),
    "footer_link_services": ("footer", "link_services"),
    "footer_link_contact": ("footer", "link_contact"),
    "footer_copyright": ("footer", "copyright"),

    "callback_title": ("callback", "title"),
    "callback_description": ("callback", "description"),
    "callback_submit": ("callback", "submit")
}

LANGUAGE_URLS = {
    "es": "/",
    "en": "/en/",
    "uk": "/uk/",
    "ru": "/ru/",
    "ro": "/ro/"
}


def get_value(data, path):
    value = data

    for key in path:
        value = value[key]

    return str(value)


def replace_element_text(document, element_id, value, keep_leading_tags=False):
    pattern = re.compile(
        rf'(<(?P<tag>[a-zA-Z0-9]+)\b(?=[^>]*\bid=["\']{re.escape(element_id)}["\'])[^>]*>)(.*?)(</(?P=tag)>)',
        re.IGNORECASE | re.DOTALL
    )

    def replacer(match):
        opening = match.group(1)
        inner = match.group(3)
        closing = match.group(4)
        escaped_value = html.escape(value, quote=False)

        if keep_leading_tags:
            prefix_match = re.match(
                r'(\s*(?:<[^>]+>\s*)+)',
                inner,
                re.DOTALL
            )

            prefix = prefix_match.group(1) if prefix_match else ""
            return opening + prefix + escaped_value + closing

        return opening + escaped_value + closing

    return pattern.sub(replacer, document, count=1)


def replace_placeholder(document, element_id, value):
    pattern = re.compile(
        rf'<input\b(?=[^>]*\bid=["\']{re.escape(element_id)}["\'])[^>]*>',
        re.IGNORECASE | re.DOTALL
    )

    def replacer(match):
        tag = match.group(0)
        escaped_value = html.escape(value, quote=True)

        if re.search(r'\bplaceholder=["\'][^"\']*["\']', tag, re.IGNORECASE):
            return re.sub(
                r'\bplaceholder=["\'][^"\']*["\']',
                f'placeholder="{escaped_value}"',
                tag,
                count=1,
                flags=re.IGNORECASE
            )

        return tag[:-1] + f' placeholder="{escaped_value}">'

    return pattern.sub(replacer, document, count=1)


def replace_language_link(document, language, url):
    pattern = re.compile(
        rf'<a\b(?=[^>]*\bdata-lang=["\']{re.escape(language)}["\'])[^>]*>',
        re.IGNORECASE
    )

    def replacer(match):
        tag = match.group(0)

        tag = re.sub(
            r'href=["\'][^"\']*["\']',
            f'href="{url}"',
            tag,
            count=1,
            flags=re.IGNORECASE
        )

        tag = re.sub(
            r'\s+data-lang=["\'][^"\']*["\']',
            '',
            tag,
            count=1,
            flags=re.IGNORECASE
        )

        return tag

    return pattern.sub(replacer, document, count=1)


def make_absolute_asset_paths(document):
    pattern = re.compile(
        r'(?P<prefix>\b(?:href|src|data-setbg)=["\'])(?P<path>(?:css|js|img|fonts)/[^"\']+)',
        re.IGNORECASE
    )

    return pattern.sub(
        lambda match: match.group("prefix") + "/" + match.group("path"),
        document
    )


def create_meta_description(data):
    if "meta_description" in data:
        description = data["meta_description"]
    elif "seo" in data and "description" in data["seo"]:
        description = data["seo"]["description"]
    else:
        description = data["about"]["description"]

    description = " ".join(description.split())

    if len(description) <= 155:
        return description

    shortened = description[:155].rsplit(" ", 1)[0]
    return shortened + "…"


def add_seo_tags(document, language, current_url):
    canonical_url = BASE_URL + current_url

    hreflang = f"""
    <link rel="canonical" href="{canonical_url}">
    <link rel="alternate" hreflang="es" href="{BASE_URL}/">
    <link rel="alternate" hreflang="en" href="{BASE_URL}/en/">
    <link rel="alternate" hreflang="uk" href="{BASE_URL}/uk/">
    <link rel="alternate" hreflang="ru" href="{BASE_URL}/ru/">
    <link rel="alternate" hreflang="ro" href="{BASE_URL}/ro/">
    <link rel="alternate" hreflang="x-default" href="{BASE_URL}/">
"""

    return document.replace("</head>", hreflang + "\n</head>", 1)


def add_callback_translations(document, language, data):
    callback_data = json.dumps(
        {"callback": data["callback"]},
        ensure_ascii=False
    ).replace("</", "<\\/")

    script = f"""
<script>
window.TemploI18n = {{
    getCurrentLanguage: () => "{language}",
    getTranslations: () => ({callback_data})
}};
</script>
"""

    callback_script = '<script src="/js/callback.js"></script>'

    return document.replace(
        callback_script,
        script + "\n" + callback_script,
        1
    )


def build_page(language, config):
    with open(TEMPLATE, "r", encoding="utf-8") as file:
        document = file.read()

    language_file = LANG_DIR / config["file"]

    with open(language_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    document = re.sub(
        r'<html\b[^>]*\blang=["\'][^"\']*["\']',
        f'<html lang="{language}"',
        document,
        count=1,
        flags=re.IGNORECASE
    )

    document = re.sub(
        r'<title>.*?</title>',
        f'<title>{html.escape(data["title"], quote=False)}</title>',
        document,
        count=1,
        flags=re.IGNORECASE | re.DOTALL
    )

    meta_description = html.escape(
        create_meta_description(data),
        quote=True
    )

    document = re.sub(
        r'(<meta\b(?=[^>]*\bname=["\']description["\'])[^>]*\bcontent=["\'])[^"\']*(["\'][^>]*>)',
        rf'\g<1>{meta_description}\g<2>',
        document,
        count=1,
        flags=re.IGNORECASE
    )

    for element_id, path in TEXT_MAP.items():
        value = get_value(data, path)

        document = replace_element_text(
            document,
            element_id,
            value,
            keep_leading_tags=(element_id == "hero_contact_btn")
        )

    document = replace_placeholder(
        document,
        "callback_name",
        data["callback"]["name_placeholder"]
    )

    document = replace_placeholder(
        document,
        "callback_phone_input",
        data["callback"]["phone_placeholder"]
    )

    for lang_code, url in LANGUAGE_URLS.items():
        document = replace_language_link(
            document,
            lang_code,
            url
        )

    document = re.sub(
        r'\s*<script\s+src=["\']/?js/i18n\.js["\']\s*></script>\s*',
        "\n",
        document,
        count=1,
        flags=re.IGNORECASE
    )

    document = make_absolute_asset_paths(document)

    document = add_seo_tags(
        document,
        language,
        config["url"]
    )

    document = add_callback_translations(
        document,
        language,
        data
    )

    output_file = config["output"]
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(document)

    print(f"{language}: {output_file.relative_to(ROOT)}")


def main():
    if not TEMPLATE.exists():
        raise FileNotFoundError(
            "Не знайдено src/index.template.html"
        )

    for language, config in LANGUAGES.items():
        build_page(language, config)

    print()
    print("Готово.")
    print("Створено:")
    print("index.html")
    print("en/index.html")
    print("uk/index.html")
    print("ru/index.html")
    print("ro/index.html")


if __name__ == "__main__":
    main()