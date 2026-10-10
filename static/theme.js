// Theme Switcher (Dark / Night Mode)
(function () {
    const savedTheme = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-theme", savedTheme);

    function updateToggleButton(btn, theme) {
        if (!btn) return;
        btn.innerHTML = theme === "dark" ? "🌙 Night" : "☀️ Light";
    }

    document.addEventListener("DOMContentLoaded", function () {
        const toggleBtn = document.getElementById("theme-toggle");
        updateToggleButton(toggleBtn, savedTheme);

        if (toggleBtn) {
            toggleBtn.addEventListener("click", function () {
                const currentTheme = document.documentElement.getAttribute("data-theme");
                const nextTheme = currentTheme === "dark" ? "light" : "dark";

                document.documentElement.setAttribute("data-theme", nextTheme);
                localStorage.setItem("theme", nextTheme);
                updateToggleButton(toggleBtn, nextTheme);
            });
        }
    });
})();

