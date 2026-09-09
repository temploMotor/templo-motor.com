document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("callbackForm");
    const submitButton = document.getElementById("callback_submit");
    const nameInput = document.getElementById("callback_name");
    const phoneInput = document.getElementById("callback_phone_input");

    if (!form || !nameInput || !phoneInput) return;

    const SERVICE_ID = "service_bz7hutl";
    const TEMPLATE_ID = "template_017e8tz";
    const PUBLIC_KEY = "Tlx58qF7qSK1DVS3j";

    function showPopup(message, type = "success") {
        const existingPopup = document.querySelector(".callback-popup-overlay");

        if (existingPopup) {
            existingPopup.remove();
        }

        const overlay = document.createElement("div");

        overlay.className = "callback-popup-overlay";

        overlay.innerHTML = `
            <div class="callback-popup">
                <div class="callback-popup__icon ${type}">
                    ${type === "success" ? "✓" : "!"}
                </div>

                <div class="callback-popup__message">
                    ${message}
                </div>

                <button class="callback-popup__button" type="button">
                    OK
                </button>
            </div>
        `;

        document.body.appendChild(overlay);

        const closePopup = () => {
            overlay.classList.add("callback-popup-overlay--hide");

            setTimeout(() => {
                overlay.remove();
            }, 250);
        };

        overlay
            .querySelector(".callback-popup__button")
            .addEventListener("click", closePopup);

        overlay.addEventListener("click", (event) => {
            if (event.target === overlay) {
                closePopup();
            }
        });
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const translations =
            window.TemploI18n?.getTranslations()?.callback;

        const successMessage =
            translations?.success ||
            "¡Todo listo! Le llamaremos.";

        const sendErrorMessage =
            translations?.send_error ||
            "No se pudo enviar la solicitud.";

        const invalidPhoneMessage =
            translations?.invalid_phone ||
            "Introduce un número de teléfono válido.";

        const name = nameInput.value.trim();
        const phone = phoneInput.value.trim();

        const allowedPhoneCharacters = /^[0-9+\s().-]+$/;
        const digitsOnly = phone.replace(/\D/g, "");

        const isPhoneValid =
            allowedPhoneCharacters.test(phone) &&
            digitsOnly.length >= 7 &&
            digitsOnly.length <= 15;

        if (!isPhoneValid) {
            showPopup(invalidPhoneMessage, "error");
            phoneInput.focus();
            return;
        }

        const currentLanguage =
            window.TemploI18n?.getCurrentLanguage() ||
            document.documentElement.lang ||
            "es";

        const languageNames = {
            es: "Español",
            en: "English",
            uk: "Українська",
            ru: "Русский",
            ro: "Română"
        };

        if (submitButton) {
            submitButton.disabled = true;
        }

        try {
            await emailjs.send(
                SERVICE_ID,
                TEMPLATE_ID,
                {
                    name: name,
                    phone: phone,
                    language:
                        languageNames[currentLanguage] ||
                        currentLanguage,
                    time: new Date().toLocaleString("uk-UA"),
                    page_url: window.location.href
                },
                {
                    publicKey: PUBLIC_KEY
                }
            );

            showPopup(successMessage, "success");

            form.reset();

        } catch (error) {
            console.error("EmailJS error:", error);

            showPopup(sendErrorMessage, "error");

        } finally {
            if (submitButton) {
                submitButton.disabled = false;
            }
        }
    });
});