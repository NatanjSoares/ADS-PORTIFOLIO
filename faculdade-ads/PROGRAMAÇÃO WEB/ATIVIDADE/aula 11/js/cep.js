const formulario = document.getElementById('formulario-cadastro');
const campoCep = document.getElementById('cep');

const getcep = async function (cep) {
    const url = `https://viacep.com.br/ws/${cep}/json/`;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Erro ${response.status}`);

        const itemcep = await response.json();

        if (itemcep.erro) {
            alert('CEP não encontrado');
            return;
        }

        document.getElementById('logradouro').value = itemcep.logradouro;
        document.getElementById('bairro').value = itemcep.bairro;
        document.getElementById('cidade').value = itemcep.localidade;
        document.getElementById('uf').value = itemcep.uf;
    } catch (erro) {
        console.error('Falha ao buscar o CEP:', erro.message);
    }
};

// busca o endereço ao sair do campo CEP
campoCep.addEventListener('blur', function () {
    const cep = campoCep.value.replace(/\D/g, '');
    if (cep.length === 8) getcep(cep);
});

// o botão Cadastrar passa a cuidar só do cadastro
formulario.addEventListener('submit', function (event) {
    event.preventDefault();
    // aqui entra o código que adiciona o cliente na lista
});