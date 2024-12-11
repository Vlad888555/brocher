<?php
$data = json_decode(file_get_contents("php://input"), true);

if ($data) {

    // Подписываем данные
    $signedData = [
        'id' => $data['id'],

        'signedAt' => date('Y-m-d H:i:s'),
        'signature' => 'Signed by server'
    ];


    echo json_encode($signedData);
} else {

    echo json_encode(['error' => 'No data received']);
}
?>