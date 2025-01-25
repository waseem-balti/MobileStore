var Base = (function() {
    // DOM Elements
    const searchModal = document.getElementById('search-modal');
    const searchButton = document.getElementById('search-button');
    const closeButton = document.getElementById('close-search');
    const modalContent = searchModal?.querySelector('.bg-white');
    const searchInput = document.querySelector('input[name="q"]');
    const suggestions = document.getElementById('search-suggestions');
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const userMenuButton = document.getElementById('user-menu-button');
    const userMenuDropdown = document.getElementById('user-menu-dropdown');

    function openModal() {
        if (searchModal) {
            searchModal.classList.remove('hidden');
            document.body.style.overflow = 'hidden'; // Disable body scroll
            searchInput?.focus();
            setTimeout(() => searchModal.classList.add('opacity-100'), 10); // Transition
        }
    }

    function closeModal() {
        if (searchModal) {
            searchModal.classList.remove('opacity-100');
            document.body.style.overflow = ''; // Re-enable body scroll
            setTimeout(() => searchModal.classList.add('hidden'), 300); // Wait for transition
            suggestions?.classList.add('hidden'); // Hide suggestions
        }
    }

    function init() {
        if (searchButton) {
            searchButton.addEventListener('click', (e) => {
                e.preventDefault();
                openModal();
            });
        }

        if (closeButton) {
            closeButton.addEventListener('click', (e) => {
                e.preventDefault();
                closeModal();
            });
        }

        if (searchModal) {
            searchModal.addEventListener('click', (e) => {
                if (!modalContent?.contains(e.target)) {
                    closeModal();
                }
            });
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !searchModal?.classList.contains('hidden')) {
                closeModal();
            }
        });

        // Handle Search Suggestions
        searchInput?.addEventListener('focus', () => {
            suggestions?.classList.remove('hidden');
        });

        document.addEventListener('click', (e) => {
            if (!searchInput?.contains(e.target) && !suggestions?.contains(e.target)) {
                suggestions?.classList.add('hidden');
            }
        });

        // Mobile Menu Toggle
        mobileMenuButton?.addEventListener('click', () => {
            mobileMenu?.classList.toggle('hidden');
        });

        // User Menu Dropdown
        if (userMenuButton && userMenuDropdown) {
            userMenuButton.addEventListener('click', (e) => {
                e.stopPropagation();
                userMenuDropdown.classList.toggle('hidden');
            });

            document.addEventListener('click', (e) => {
                if (!userMenuDropdown.contains(e.target) && !userMenuButton.contains(e.target)) {
                    userMenuDropdown.classList.add('hidden');
                }
            });

            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    userMenuDropdown.classList.add('hidden');
                }
            });
        }
    }

    return {
        init: init
    };
})();

document.addEventListener('DOMContentLoaded', Base.init);