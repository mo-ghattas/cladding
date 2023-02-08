<?php


if ($_SERVER['REQUEST_METHOD'] != "POST") {
    include dirname(__FILE__, 2) . '/templates/page404.php';
    exit();
}
