const showData = (result) => {
    for (const tabela in result) {
        if (document.querySelector("#" + tabela)) {
            document.querySelector("#" + tabela).value = result[tabela]
        }

    }
}

var requestOptions = {
    method: 'GET',
    redirect: 'follow'
};
fetch(`http://localhost:8080/wanteds`, {
        method: 'GET',
        mode: 'cors',
    })
    .then(data => showData(data))
    .then(response => response.json())
    .then(data => {
        let dadosProcurados = data;
        atualizarUI(dadosProcurados);
    })
    .catch(error => {
        console.error('Erro:', error);
    });