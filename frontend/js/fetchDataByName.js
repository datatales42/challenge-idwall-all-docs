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
                const h2SoughtBy = document.getElementById('soughtBy');
                if (wanted.wanted_origin === 'FBI') {
                    fbiLogo.style.display = 'block'; // Exibe o logo do FBI
                    interpolLogo.style.display = 'none'; // Oculta o logo da Interpol
                    h2SoughtBy.textContent = 'Sought by the FBI';
                } else if (wanted.wanted_origin === 'INTERPOL') {
                    fbiLogo.style.display = 'none'; // Oculta o logo do FBI
                    interpolLogo.style.display = 'block'; // Exibe o logo da Interpol
                    h2SoughtBy.textContent = 'Sought by the Interpol';
                } else {
                    fbiLogo.style.display = 'none'; // Oculta o logo do FBI
                    interpolLogo.style.display = 'none'; // Oculta o logo da Interpol
                    h2SoughtBy.textContent = '';
                }
                // Atualize o conteúdo da div "wantedData" com os detalhes do "wanted"
                document.getElementById('wantedData').innerHTML = `
                <p>Wanted_origin_id: ${wanted.wanted_origin_id} </p>
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
                <p>sex: ${wanted.sex}</p>
                <p>weight: ${wanted.weight}</p>
                <p>wanted_origin: ${wanted.wanted_origin}</p>
                <p>age_range: ${wanted.age_range}</p>
                <p>aliases: ${wanted.aliases}</p>
                <p>ncic: ${wanted.ncic}</p>
                <p>age_max: ${wanted.age_max}</p>
                <p>age_min: ${wanted.age_min}</p>
                <p>build: ${wanted.build}</p>
                <p>complexion: ${wanted.complexion}</p>
                <p>details: ${wanted.details}</p>
                <p>eyes_raw: ${wanted.eyes_raw}</p>
                <p>field_offices: ${wanted.field_offices}</p>
                <p>hair_raw: ${wanted.hair_raw}</p>
                <p>height_max: ${wanted.height_max}</p>
                <p>height_min: ${wanted.height_min}</p>
                <p>modified: ${wanted.modified}</p>
                <p>occupations: ${wanted.occupations}</p>
                <p>person_classification: ${wanted.person_classification}</p>
                <p>possible_countries: ${wanted.possible_countries}</p>
                <p>possible_states: ${wanted.possible_states}</p>
                <p>poster_classification: ${wanted.poster_classification}</p>
                <p>publication: ${wanted.publication}</p>
                <p>race: ${wanted.race}</p>
                <p>race_raw: ${wanted.race_raw}</p>
                <p>remarks: ${wanted.remarks}</p>
                <p>reward_text: ${wanted.reward_text}</p>
                <p>status: ${wanted.status}</p>
                <p>subjects: ${wanted.subjects}</p>
                <p>suspects: ${wanted.suspects}</p>
                <p>title: ${wanted.title}</p>
                <p>url: ${wanted.url}</p>
                <p>warning_message: ${wanted.warning_message}</p>
                <p>weight_max: ${wanted.weight_max}</p>
                <p>weight_min: ${wanted.weight_min}</p>
                <p>analyzed_at: ${wanted.analyzed_at}</p>
                `;
                // Remova a classe "wantedData-header" para mostrar o card
                document.querySelector('.wantedData-header').style.display = 'flex';
                // Oculte o elemento de erro
                document.getElementById('error-message').style.display = 'none';
            } else {
                // Exiba a mensagem de erro
                document.getElementById('error-message').textContent = 'Registro não encontrado.';
                document.getElementById('error-message').style.display = 'block';
                // Oculte a classe "wantedData-header"
                document.querySelector('.wantedData-header').style.display = 'none';
            }
        })
        .catch(error => console.error('Erro:', error));
}

function closeCard() {
    // Adicione a classe "wantedData-header" para ocultar o card
    document.querySelector('.wantedData-header').style.display = 'none';
}

// Adicionar evento para ocultar a mensagem de erro quando o campo de entrada for esvaziado
document.getElementById('searchInput').addEventListener('input', function() {
    if (this.value === '') {
        document.getElementById('error-message').style.display = 'none';
    }
});
