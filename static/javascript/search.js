
    function hoverResult(element) {
        element.style.backgroundColor = '#f5f5f5'; // Set your desired hover background color
    }

    function unhoverResult(element) {
        element.style.backgroundColor = ''; // Reset to the default background color
    }

    function loadValueToSearchInput(value) {
        document.getElementById('searchInput').value = value;
    }

    new Autocomplete('#autocomplete', {
        search: input => {
            console.log(input);

            if (!input) {
                return Promise.resolve([]);
            }

            const url = `/get-names/?search=${encodeURIComponent(input)}`;

            return fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => data.payload)
                .catch(error => {
                    console.error('Error fetching data:', error);
                    return [];
                });
        },
        renderResult: (result, props) => {
            console.log(props);

            let group = '';
            if (props && props.index % 3 === 0) {
                group = `<li style="background-color: #f0f0f0; padding: 5px; font-weight: bold; color: #333;">Group</li>`;
            }

            if (!result || result.length === 0) {
                return `${group}<li style="list-style: none; padding: 10px; text-align: center;">No result found</li>`;
            }

            // Accessing the username from the props object
            const username = props.username || result.user;

            // Adding a hyperlink to the li element
            const profileLink = `/view_profile/${username}/`;

            return `
                ${group}
                <li style="list-style: none; padding: 10px; border-bottom: 1px solid #ddd; cursor: pointer; transition: background-color 0.3s;" 
                    onclick="loadValueToSearchInput('${username}')"
                    onmouseover="hoverResult(this)"
                    onmouseout="unhoverResult(this)">
                    <a href="${profileLink}" style="text-decoration: none; color: inherit;">
                        <div style="font-size: 16px; color: #007bff;" class="wiki-title">
                            ${username}
                        </div>
                    </a>
                </li>`;
        }
    });

