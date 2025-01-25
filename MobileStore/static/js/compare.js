var Compare = (function() {
    const compareMenuButton = document.getElementById('compare-menu-button');
    const compareDropdown = document.getElementById('compare-dropdown');

    function openCompareModal(type) {
        compareDropdown?.classList.add('hidden');
        
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-gray-800 bg-opacity-75 backdrop-blur-sm flex items-center justify-center z-50';
        modal.id = 'compareModal';

        const compareUrls = {
            phone: '/compare_phones/',
            laptop: '/compare_laptops/',
            accessory: '/compare_accessories/'
        };

        modal.innerHTML = `
            <div class="bg-white rounded-xl shadow-2xl p-6 w-full max-w-3xl mx-4">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold text-gray-900">Compare ${type.charAt(0).toUpperCase() + type.slice(1)}s</h2>
                    <button onclick="Compare.closeCompareModal()" class="text-gray-400 hover:text-gray-600">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                    </button>
                </div>

                <form id="compareForm" action="${compareUrls[type]}" method="GET">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                        <!-- First Product -->
                        <div class="relative">
                            <label class="block text-sm font-medium text-gray-700 mb-2">First ${type}</label>
                            <input type="hidden" name="${type}" id="product1_id">
                            <input type="text" 
                                   id="product1_search"
                                   class="w-full px-4 py-2.5 border-2 border-gray-200 rounded-lg"
                                   placeholder="Search ${type}..."
                                   autocomplete="off"
                                   oninput="Compare.searchProducts(this.value, '1', '${type}')">
                            <div id="results1" class="absolute z-50 w-full mt-1 bg-white rounded-lg shadow-lg max-h-60 overflow-y-auto hidden"></div>
                        </div>

                        <!-- Second Product -->
                        <div class="relative">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Second ${type}</label>
                            <input type="hidden" name="${type}" id="product2_id">
                            <input type="text" 
                                   id="product2_search"
                                   class="w-full px-4 py-2.5 border-2 border-gray-200 rounded-lg"
                                   placeholder="Search ${type}..."
                                   autocomplete="off"
                                   oninput="Compare.searchProducts(this.value, '2', '${type}')">
                            <div id="results2" class="absolute z-50 w-full mt-1 bg-white rounded-lg shadow-lg max-h-60 overflow-y-auto hidden"></div>
                        </div>
                    </div>

                    <div class="flex justify-end space-x-3">
                        <button type="button" onclick="Compare.closeCompareModal()" 
                                class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200">
                            Cancel
                        </button>
                        <button type="submit" 
                                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                            Compare
                        </button>
                    </div>
                </form>
            </div>
        `;

        document.body.appendChild(modal);

        // Add form submit handler
        document.getElementById('compareForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const id1 = document.getElementById('product1_id').value;
            const id2 = document.getElementById('product2_id').value;

            if (!id1 || !id2) {
                alert('Please select two products to compare');
                return;
            }

            window.location.href = `${compareUrls[type]}?${type}=${id1}&${type}=${id2}`;
        });
    }

    async function searchProducts(query, num, type) {
        const resultsDiv = document.getElementById(`results${num}`);
        
        if (query.length < 2) {
            resultsDiv.classList.add('hidden');
            return;
        }

        try {
            const response = await fetch(`/search_${type}s/?q=${encodeURIComponent(query)}`);
            if (!response.ok) throw new Error('Network response was not ok');
            
            const products = await response.json();
            
            resultsDiv.innerHTML = products.map(product => `
                <div class="p-3 hover:bg-gray-50 cursor-pointer flex items-center space-x-3"
                     onclick="Compare.selectProduct('${num}', '${product.id}', '${product.name}')">
                    <img src="${product.images?.[0]?.image || '/static/images/placeholder.png'}" 
                         class="w-12 h-12 object-contain rounded" 
                         alt="${product.name}">
                    <div>
                        <div class="font-medium">${product.name}</div>
                        <div class="text-sm text-gray-500">
                            PKR ${product.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}
                        </div>
                    </div>
                </div>
            `).join('');
            
            resultsDiv.classList.remove('hidden');
        } catch (error) {
            console.error('Error searching products:', error);
            resultsDiv.innerHTML = '<div class="p-3 text-red-600">Error loading results</div>';
        }
    }

    function selectProduct(num, id, name) {
        document.getElementById(`product${num}_search`).value = name;
        document.getElementById(`product${num}_id`).value = id;
        document.getElementById(`results${num}`).classList.add('hidden');
    }

    function closeCompareModal() {
        const modal = document.getElementById('compareModal');
        if (modal) modal.remove();
    }

    function init() {
        compareMenuButton?.addEventListener('click', (e) => {
            e.stopPropagation();
            compareDropdown?.classList.toggle('hidden');
        });

        document.addEventListener('click', (e) => {
            if (!compareDropdown?.contains(e.target) && !compareMenuButton?.contains(e.target)) {
                compareDropdown?.classList.add('hidden');
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                compareDropdown?.classList.add('hidden');
                closeCompareModal();
            }
        });
    }

    return {
        init: init,
        openCompareModal: openCompareModal,
        searchProducts: searchProducts,
        selectProduct: selectProduct,
        closeCompareModal: closeCompareModal
    };
})();

document.addEventListener('DOMContentLoaded', Compare.init);