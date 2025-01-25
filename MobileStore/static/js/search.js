var Search = (function() {
    function searchPhones(input, resultContainerId) {
        const query = input.value;
        if (query.length < 2) {
            document.getElementById(resultContainerId).classList.add('hidden');
            return;
        }

        fetch(`/search_phones/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                const resultContainer = document.getElementById(resultContainerId);
                resultContainer.innerHTML = '';
                data.forEach(phone => {
                    const option = document.createElement('div');
                    option.className = 'p-4 hover:bg-gray-50 cursor-pointer flex items-center space-x-3';
                    option.innerHTML = `
                        <img src="${phone.images ? phone.images[0].image : '/static/images/placeholder.png'}" 
                             alt="${phone.name}" 
                             class="w-10 h-10 object-contain rounded">
                        <div>
                            <div class="font-medium">${phone.name}</div>
                            <div class="text-sm text-gray-500">
                                PKR ${phone.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}
                            </div>
                        </div>
                    `;
                    option.onclick = () => {
                        input.value = phone.name;
                        document.getElementById(`${input.id}_id`).value = phone.id;
                        resultContainer.classList.add('hidden');
                    };
                    resultContainer.appendChild(option);
                });
                resultContainer.classList.remove('hidden');
            });
    }

    function searchAccessories(input, resultContainerId) {
        const query = input.value;
        if (query.length < 2) {
            document.getElementById(resultContainerId).classList.add('hidden');
            return;
        }

        fetch(`/search_accessories/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                const resultContainer = document.getElementById(resultContainerId);
                resultContainer.innerHTML = '';
                data.forEach(accessory => {
                    const option = document.createElement('div');
                    option.className = 'p-4 hover:bg-gray-50 cursor-pointer flex items-center space-x-3';
                    option.innerHTML = `
                        <img src="${accessory.images ? accessory.images[0].image : '/static/images/placeholder.png'}" 
                             alt="${accessory.name}" 
                             class="w-10 h-10 object-contain rounded">
                        <div>
                            <div class="font-medium">${accessory.name}</div>
                            <div class="text-sm text-gray-500">
                                PKR ${accessory.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}
                            </div>
                        </div>
                    `;
                    option.onclick = () => {
                        input.value = accessory.name;
                        document.getElementById(`${input.id}_id`).value = accessory.id;
                        resultContainer.classList.add('hidden');
                    };
                    resultContainer.appendChild(option);
                });
                resultContainer.classList.remove('hidden');
            });
    }

    function searchLaptops(input, resultContainerId) {
        const query = input.value;
        if (query.length < 2) {
            document.getElementById(resultContainerId).classList.add('hidden');
            return;
        }

        fetch(`/search_laptops/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                const resultContainer = document.getElementById(resultContainerId);
                resultContainer.innerHTML = '';
                data.forEach(laptop => {
                    const option = document.createElement('div');
                    option.className = 'p-4 hover:bg-gray-50 cursor-pointer flex items-center space-x-3';
                    option.innerHTML = `
                        <img src="${laptop.images ? laptop.images[0].image : '/static/images/placeholder.png'}" 
                             alt="${laptop.name}" 
                             class="w-10 h-10 object-contain rounded">
                        <div>
                            <div class="font-medium">${laptop.name}</div>
                            <div class="text-sm text-gray-500">
                                PKR ${laptop.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}
                            </div>
                        </div>
                    `;
                    option.onclick = () => {
                        input.value = laptop.name;
                        document.getElementById(`${input.id}_id`).value = laptop.id;
                        resultContainer.classList.add('hidden');
                    };
                    resultContainer.appendChild(option);
                });
                resultContainer.classList.remove('hidden');
            });
    }

    return {
        searchPhones: searchPhones,
        searchAccessories: searchAccessories,
        searchLaptops: searchLaptops
    };
})();