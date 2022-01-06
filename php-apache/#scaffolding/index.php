<?php
require __DIR__ . "/vendor/autoload.php";
$router = new \Bramus\Router\Router();

/** HOME */
$router->get('/', function () {
    require __DIR__ . '/pages/home.php';
});


/** POST */
// $router->get('/{postid}/{title}', function ($postid, $title) {
//     $_GET['postid'] = $postid;
//     require __DIR__ . '/pages/post.php';
// });

$router->set404(function () {
    header('HTTP/1.1 404 Not Found');
    require __DIR__ . '/pages/404-page-not-found.php';
});

$router->run();
