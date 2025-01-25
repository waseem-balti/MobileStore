var Modal = (function() {
    function openCompareModal() {
        document.getElementById('compareModal').classList.remove('hidden');
        document.addEventListener('keydown', handleEscKey);
    }

    function closeCompareModal() {
        document.getElementById('compareModal').classList.add('hidden');
        document.removeEventListener('keydown', handleEscKey);
    }

    function handleEscKey(e) {
        if (e.key === 'Escape') {
            closeCompareModal();
        }
    }

    return {
        openCompareModal: openCompareModal,
        closeCompareModal: closeCompareModal,
        handleEscKey: handleEscKey
    };
})();