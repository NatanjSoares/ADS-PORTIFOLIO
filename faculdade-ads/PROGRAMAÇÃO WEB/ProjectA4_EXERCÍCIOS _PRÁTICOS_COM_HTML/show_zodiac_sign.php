<?php include('layouts/header.php'); ?>
<body class="bg-light">
<div class="container mt-5">
<?php
// 1) Recebe a data do formulário (formato AAAA-MM-DD)
$data_nascimento = $_POST['data_nascimento'];

// 2) Carrega o XML
$signos = simplexml_load_file("signos.xml");

// 3) Converte "21/03" em uma data válida usando o ano informado
function converterData($diaMes, $ano) {
    return DateTime::createFromFormat('!d/m/Y', $diaMes . '/' . $ano);
}

$nascimento = new DateTime($data_nascimento);
$ano = $nascimento->format('Y');
$signoEncontrado = null;

// 4) Percorre cada signo e testa se a data cai no intervalo
foreach ($signos->signo as $signo) {
    $inicio = converterData((string) $signo->dataInicio, $ano);
    $fim    = converterData((string) $signo->dataFim, $ano);

    // Caso especial: signo que cruza o ano (Capricórnio)
    if ($inicio > $fim) {
        if ($nascimento >= $inicio) {
            $fim->modify('+1 year');
        } else {
            $inicio->modify('-1 year');
        }
    }

    if ($nascimento >= $inicio && $nascimento <= $fim) {
        $signoEncontrado = $signo;
        break;
    }
}
?>

<?php if ($signoEncontrado): ?>
    <div class="card text-center shadow mx-auto" style="max-width: 500px;">
        <div class="card-body">
            <h2 class="card-title"><?= $signoEncontrado->signoNome ?></h2>
            <h6 class="text-muted">
                <?= $signoEncontrado->dataInicio ?> a <?= $signoEncontrado->dataFim ?>
            </h6>
            <p class="card-text mt-3"><?= $signoEncontrado->descricao ?></p>
            <a href="index.php" class="btn btn-secondary">Voltar</a>
        </div>
    </div>
<?php else: ?>
    <div class="alert alert-danger text-center">Signo não encontrado.</div>
    <div class="text-center"><a href="index.php" class="btn btn-secondary">Voltar</a></div>
<?php endif; ?>
</div>
</body>
</html>