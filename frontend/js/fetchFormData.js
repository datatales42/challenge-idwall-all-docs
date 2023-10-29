const radioButtonEquals = document.getElementById('exact-match-true');
const radioButtonContains = document.getElementById('exact-match-false');

function toggleRadioSelection() {

    if (radioButtonEquals.checked) {
        radioButtonEquals.checked = false;
        radioButtonContains.checked = true;
    } else if (radioButtonContains.checked) {
        radioButtonContains.checked = false;
        radioButtonEquals.checked = true;
    }
}



function fetchFormData() {
    event.preventDefault()

    var alias = document.getElementById('searchName').value;
    var exact_match = radioButtonEquals.checked
    var birthdate = document.getElementById('searchBirthDate').value;
    var distinguishing_marks = document.getElementById('searchMarks').value;
    var nationality = document.getElementById('searchNationality').value;
    var languages = document.getElementById('searchLanguages').value;
    var sex = document.getElementById('searchSex').value;
    var wanted_in = document.getElementById('searchWantedIn').value;
    var charges = document.getElementById('searchCharges').value;
    
    console.log(`
    Search Parameters:
    alias = ${alias}
    exact_match = ${exact_match}
    birthdate = ${birthdate}
    distinguishing_marks = ${distinguishing_marks}
    nationality = ${nationality}
    languages = ${languages}
    sex = ${sex}
    wanted_in = ${wanted_in}
    charges = ${charges}
    `)
    var url = 'http://localhost:8080/wanteds';
    var parameters = [
        { key: 'alias', value: alias },
        { key: 'birth_date', value: birthdate },
        { key: 'distinguishing_marks', value: distinguishing_marks },
        { key: 'nationality', value: nationality },
        { key: 'languages', value: languages },
        { key: 'sex', value: sex },
        { key: 'wanted_in', value: wanted_in },
        { key: 'charges', value: charges }
    ];
    
    var queryParams = parameters
    .filter(param => param.value !== '')
    .map(param => `${param.key}=${encodeURIComponent(param.value)}`)
    .join('&');
    
    if (queryParams !== '') {
        url += '?' + queryParams;
        if(alias !== ''){
            url += '&exact_match=' + exact_match;
        }
    }
    console.log(url)
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data && data.potential_matches && data.potential_matches.length > 0) {

                document.getElementById('num-matches-found').innerHTML = data.potential_matches.length + ' matches found'

                for(let i = 0; i < data.potential_matches.length; i++){
                    const wanted = data.potential_matches[i];
                    //console.log(wanted)

                    var innerContent = `
                        <div class="wantedData-header-form mb-5">
                            <div class="logo-container">
                                <!-- wanted_origin_image -->
                                <!-- sought_by -->
                            </div>
                            <div id="wantedDataContent" class="mb-5">
                                <!-- wanted_data -->
                            </div>
                        </div>`

                    // Verifique a origem do "wanted" e mostre a imagem correspondente
                    if (wanted.wanted_origin === 'FBI') {
                        innerContent = innerContent.replace('<!-- wanted_origin_image -->', '<img class="wantedData-header-img" id="fbiLogo" src="../assets/FBI_SHIELD-logo-2D02BDDAC8-seeklogo.com.png" alt="">')
                        innerContent = innerContent.replace('<!-- sought_by -->', '<h2 id="soughtBy" >Sought by the FBI</h2>')
                    } else if (wanted.wanted_origin === 'INTERPOL') {
                        innerContent = innerContent.replace('<!-- wanted_origin_image -->', '<img class="wantedData-header-img" id="interpolLogo" src="../assets/INTERPOL_Logo.png" alt="">')
                        innerContent = innerContent.replace('<!-- sought_by -->', '<h2 id="soughtBy" >Sought by Interpol</h2>')
                    } else {
                        continue 
                    }
                    var wantedFields = [
                        { key: 'Images', value: wanted.images },
                        { key: 'Wanted Origin ID', value: wanted.wanted_origin_id },
                        { key: 'Aliases', value: wanted.aliases },
                        { key: 'Nationality', value: wanted.nationality },
                        { key: 'Place of Birth', value: wanted.place_of_birth },
                        { key: 'Age Range', value: wanted.age_range },
                        { key: 'Sex', value: wanted.sex },
                        { key: 'Charges', value: wanted.charges },
                        { key: 'Dates of Birth Used', value: wanted.dates_of_birth_used },
                        { key: 'Distinguishing Marks', value: wanted.distinguishing_marks },
                        { key: 'Eyes Color', value: wanted.eyes_color },
                        { key: 'Forename', value: wanted.forename },
                        { key: 'Hair Color', value: wanted.hair_color },
                        { key: 'Height', value: wanted.height },
                        { key: 'Issuing Country ID', value: wanted.issuing_country_id },
                        { key: 'Languages', value: wanted.languages },
                        { key: 'Name', value: wanted.name },
                        { key: 'Weight', value: wanted.weight },
                        { key: 'NCIC', value: wanted.ncic },
                        { key: 'Build', value: wanted.build },
                        { key: 'Complexion', value: wanted.complexion },
                        { key: 'Details', value: wanted.details },
                        { key: 'Eyes Raw', value: wanted.eyes_raw },
                        { key: 'Field Offices', value: wanted.field_offices },
                        { key: 'Hair Raw', value: wanted.hair_raw },
                        { key: 'Age Max', value: wanted.age_max },
                        { key: 'Age Min', value: wanted.age_min },
                        { key: 'Height Max', value: wanted.height_max },
                        { key: 'Height Min', value: wanted.height_min },
                        { key: 'Modified', value: wanted.modified },
                        { key: 'Occupations', value: wanted.occupations },
                        { key: 'Person Classification', value: wanted.person_classification },
                        { key: 'Possible Countries', value: wanted.possible_countries },
                        { key: 'Possible States', value: wanted.possible_states },
                        { key: 'Poster Classification', value: wanted.poster_classification },
                        { key: 'Publication', value: wanted.publication },
                        { key: 'Race', value: wanted.race },
                        { key: 'Race Raw', value: wanted.race_raw },
                        { key: 'Remarks', value: wanted.remarks },
                        { key: 'Reward Text', value: wanted.reward_text },
                        { key: 'Status', value: wanted.status },
                        { key: 'Subjects', value: wanted.subjects },
                        { key: 'Suspects', value: wanted.suspects },
                        { key: 'Title', value: wanted.title },
                        { key: 'URL', value: wanted.url },
                        { key: 'Warning Message', value: wanted.warning_message },
                        { key: 'Weight Max', value: wanted.weight_max },
                        { key: 'Weight Min', value: wanted.weight_min },
                        { key: 'Last Updated', value: wanted.analyzed_at }
                    ];
                    
                    var fieldsToShow = wantedFields
                        .filter(field => field.value !== '' && field.value !== null && field.value !== 'nan')
                        .map(field => {
                            if(field.key == 'Images'){
                                var regex = /'large': '([^']+)'/; // Regular expression to capture the URL after 'large'
                                var match = field.value.match(regex); // Find the match                                
                                imgUrl = match[1]
                                return `<img src="${imgUrl}" class="content-wanted-image">`
                            } else {
                                return `<p><b>${field.key}</b>: ${field.value}</p>`
                            }
                        })
                        .join(' ');

                    //console.log(fieldsToShow)
                    innerContent = innerContent.replace('<!-- wanted_data -->', fieldsToShow);
                    document.getElementById('real-content').innerHTML += innerContent 
                    document.getElementById('error-message').style.display = 'none';
                }
                // Remova a classe "wantedData-header-form" para mostrar o card
                // Select all elements with the class 'wantedData-header-form' and set their display style to 'flex'
                document.querySelectorAll('.wantedData-header-form').forEach(element => element.style.display = 'flex');
                
            } else {
                // Exiba a mensagem de erro
                document.getElementById('error-message').textContent = 'Registro não encontrado.';
                document.getElementById('error-message').style.display = 'block';
                // Oculte a classe "wantedData-header-form"
                document.querySelector('.wantedData-header-form').style.display = 'none';
            }
        })
        .catch(error => console.error('Erro:', error));

    }

/*
// Adicionar evento para ocultar a mensagem de erro quando o campo de entrada for esvaziado
document.getElementById('searchInput').addEventListener('input', function() {
    if (this.value === '') {
        document.getElementById('error-message').style.display = 'none';
    }
});*/
