function fetchDataByName() {
    const name = document.getElementById('searchInput').value;
    const url = `http://localhost:8080/wanteds?alias=${name}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data && data.potential_matches && data.potential_matches.length > 0) {
                const wanted = data.potential_matches[0];
                // Verifique a origem do "wanted" e mostre a imagem correspondente
                const fbiLogo = document.getElementById('fbiLogo');
                const interpolLogo = document.getElementById('interpolLogo');
                if (wanted.wanted_origin === 'FBI') {
                    fbiLogo.style.display = 'block'; // Exibe o logo do FBI
                    interpolLogo.style.display = 'none'; // Oculta o logo da Interpol
                } else if (wanted.wanted_origin === 'INTERPOL') {
                    fbiLogo.style.display = 'none'; // Oculta o logo do FBI
                    interpolLogo.style.display = 'block'; // Exibe o logo da Interpol
                } else {
                    fbiLogo.style.display = 'none'; // Oculta o logo do FBI
                    interpolLogo.style.display = 'none'; // Oculta o logo da Interpol
                }
                // Atualize o conteúdo da div "wantedData" com os detalhes do "wanted"
                document.getElementById('wantedData').innerHTML = `
                    <p>Name: ${wanted.name}</p>
                    <p>Wanted_origin_id: ${wanted.wanted_origin_id}</p>
                    <p>Charges: ${wanted.charges}</p>
                    <p>Nationality: ${wanted.nationality}</p>
                    <p>dates_of_birth_used: ${wanted.dates_of_birth_used}</p>
                    <p>distinguishing_marks: ${wanted.distinguishing_marks}</p>
                    <p>eyes_color: ${wanted.eyes_color}</p>
                    <p>forename: ${wanted.forename}</p>
                    <p>hair_color: ${wanted.hair_color}</p>
                    <p>height: ${wanted.height}</p>
                    <p>images: ${wanted.images}</p>
                    <p>issuing_country_id: ${wanted.issuing_country_id}</p>
                    <p>languages: ${wanted.languages}</p>
                    <p>name: ${wanted.name}</p>
                    <p>place_of_birth: ${wanted.place_of_birth}</p>
                    <p>wanted_origin: ${wanted.wanted_origin}</p>
                    <!-- Adicione outras informações que deseja exibir -->
                `;
                // Exiba o popup somente se houver dados
                showPopup();
            } else {
                document.getElementById('wantedData').innerHTML = 'Registro não encontrado.';
                document.querySelector('.wantedData-header').style.display = 'none'; // Oculta o card
            }
        })
        .catch(error => console.error('Erro:', error));
}

function showPopup() {
    // Exibe o popup
    document.getElementById('popup').style.display = 'block';
}

function closeCard() {
    document.getElementById('popup').style.display = 'none';
}
