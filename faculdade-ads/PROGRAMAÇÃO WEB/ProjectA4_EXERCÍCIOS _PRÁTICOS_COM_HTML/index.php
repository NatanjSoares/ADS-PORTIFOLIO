<?php include('layouts/header.php'); ?>
<body class="bg-light">
    <div class="container mt-5">
        <h1 class="text-center mb-4">✨ Descubra seu Signo ✨</h1>

        <div class="row justify-content-center">
            <div class="col-md-5">
                <form id="signo-form" method="POST" action="show_zodiac_sign.php" class="card p-4 shadow">
                    <label for="data_nascimento" class="form-label">Data de nascimento</label>
                    <input type="date" class="form-control mb-3" id="data_nascimento"
                           name="data_nascimento" required>
                    <button type="submit" class="btn btn-primary w-100">Consultar</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>