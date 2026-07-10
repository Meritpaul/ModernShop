/* =====================================================
    MAIN.JS
   ===================================================== */

/* =====================================================
    AOS — Initialize
   ===================================================== */

document.addEventListener("DOMContentLoaded", () => {

    if (typeof AOS !== "undefined") {
        AOS.init({
            duration: 800,
            once: true,
            offset: 80,
        });
    }

});

/* =====================================================
    PRELOADER
   ===================================================== */

window.addEventListener("load", () => {

    const preloader = document.getElementById("preloader");

    if (preloader) {
        preloader.classList.add("hide");
    }

});

/* =====================================================
    THEME TOGGLE
   ===================================================== */

const themeToggle = document.getElementById("themeToggle");

if (themeToggle) {

    // Apply saved theme on page load
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
        themeToggle.innerHTML = '<i class="bi bi-sun-fill"></i>';
    } else {
        themeToggle.innerHTML = '<i class="bi bi-moon-fill"></i>';
    }

    // Toggle on click
    themeToggle.addEventListener("click", () => {

        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
            themeToggle.innerHTML = '<i class="bi bi-sun-fill"></i>';
        } else {
            localStorage.setItem("theme", "light");
            themeToggle.innerHTML = '<i class="bi bi-moon-fill"></i>';
        }

    });

}

/* =====================================================
    STICKY NAVBAR
   ===================================================== */

window.addEventListener("scroll", () => {

    const navbar = document.querySelector(".custom-navbar");

    if (navbar) {
        navbar.classList.toggle("scrolled", window.scrollY > 80);
    }

});

/* =====================================================
    CLOSE MOBILE NAVBAR ON LINK CLICK
   ===================================================== */

document.addEventListener("DOMContentLoaded", () => {

    const navLinks = document.querySelectorAll(".navbar-nav .nav-link");
    const navCollapse = document.getElementById("navbarMain");

    if (navCollapse) {
        navLinks.forEach(link => {
            link.addEventListener("click", () => {
                // Only collapse on mobile (when toggler is visible)
                if (window.innerWidth < 992) {
                    const bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
                    if (bsCollapse) bsCollapse.hide();
                }
            });
        });
    }

});

/* =====================================================
    ACTIVE NAV LINK — highlight based on current page
   ===================================================== */

document.addEventListener("DOMContentLoaded", () => {

    const currentPath = window.location.pathname;

    document.querySelectorAll(".navbar-nav .nav-link").forEach(link => {
        const href = link.getAttribute("href");
        if (href && href !== "#" && href === currentPath) {
            link.classList.add("active");
        }
    });

});

/* =====================================================
    HERO SWIPER SLIDER
   ===================================================== */

if (document.querySelector(".heroSwiper")) {

    new Swiper(".heroSwiper", {

        loop: true,
        speed: 1000,

        autoplay: {
            delay: 4000,
            disableOnInteraction: false,
        },

        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },

        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },

    });

}

/* =====================================================
    NAVBAR DARK MODE — fix text/icon colors on scroll
   ===================================================== */

document.addEventListener("DOMContentLoaded", () => {

    // Ensure navbar icon links inherit correct color in dark mode
    const updateNavIconColors = () => {
        const isDark = document.body.classList.contains("dark-mode");
        document.querySelectorAll(".navbar .text-dark").forEach(el => {
            el.style.color = isDark ? "#fff" : "";
        });
    };

    updateNavIconColors();

    if (themeToggle) {
        themeToggle.addEventListener("click", updateNavIconColors);
    }

});

/* =====================================================
    NEWSLETTER FORM — basic submit handler
   ===================================================== */

document.addEventListener("DOMContentLoaded", () => {

    const newsletterBtn = document.getElementById("newsletterBtn");
    const newsletterEmail = document.getElementById("newsletterEmail");

    if (newsletterBtn && newsletterEmail) {
        newsletterBtn.addEventListener("click", () => {
            const email = newsletterEmail.value.trim();
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (!email || !emailRegex.test(email)) {
                newsletterEmail.style.outline = "2px solid crimson";
                newsletterEmail.focus();
                return;
            }

            newsletterEmail.style.outline = "";
            newsletterBtn.textContent = "Subscribed ✓";
            newsletterBtn.disabled = true;
            newsletterEmail.value = "";
        });

        // Clear error outline on input
        newsletterEmail.addEventListener("input", () => {
            newsletterEmail.style.outline = "";
        });
    }

});

/* =====================================================
    BACK TO TOP BUTTON
   ===================================================== */

document.addEventListener("DOMContentLoaded", () => {

    // Create button
    const btn = document.createElement("button");
    btn.id = "backToTop";
    btn.innerHTML = '<i class="bi bi-arrow-up"></i>';
    btn.setAttribute("aria-label", "Back to top");
    btn.style.cssText = `
        position: fixed;
        bottom: 90px;
        right: 25px;
        width: 45px;
        height: 45px;
        border-radius: 50%;
        background: #111;
        color: #fff;
        border: none;
        font-size: 18px;
        cursor: pointer;
        display: none;
        align-items: center;
        justify-content: center;
        z-index: 9998;
        transition: opacity 0.3s, transform 0.3s;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
    `;
    document.body.appendChild(btn);

    window.addEventListener("scroll", () => {
        if (window.scrollY > 400) {
            btn.style.display = "flex";
            btn.style.opacity = "1";
        } else {
            btn.style.opacity = "0";
            setTimeout(() => {
                if (window.scrollY <= 400) btn.style.display = "none";
            }, 300);
        }
    });

    btn.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

});

/* =====================================================
    SHOW / HIDE PASSWORD TOGGLE
   ===================================================== */

function togglePassword(el) {
    const input = el.parentElement.querySelector("input");
    const icon  = el.querySelector("i");
    if (!input) return;

    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove("bi-eye");
        icon.classList.add("bi-eye-slash");
    } else {
        input.type = "password";
        icon.classList.remove("bi-eye-slash");
        icon.classList.add("bi-eye");
    }
}

/* =====================================================
    FLOATING MINI CART — auto-open after add/remove/update
   ===================================================== */

document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    if (params.get("cart") === "open") {
        const el = document.getElementById("miniCartOffcanvas");
        if (el && window.bootstrap) {
            const offcanvas = window.bootstrap.Offcanvas.getOrCreateInstance(el);
            offcanvas.show();
        }
        // clean the ?cart=open param out of the URL without reloading
        params.delete("cart");
        const newQuery = params.toString();
        const newUrl = window.location.pathname + (newQuery ? "?" + newQuery : "") + window.location.hash;
        window.history.replaceState({}, "", newUrl);
    }
});