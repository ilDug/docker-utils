#!bash

cp ./\#scaffolding/.htaccess ./
cp ./\#scaffolding/Dockerfile ./
cp ./\#scaffolding/webpack.config.js ./
cp ./\#scaffolding/index.php ./
cp ./\#scaffolding/home.php ./pages/
cp ./\#scaffolding/styles.scss ./src/styles/
cp ./\#scaffolding/_variables.scss ./src/styles/


echo "<h1>DAG NOT FOUND</h1>" > ./pages/404-page-not-found.php
echo " " > ./pages/views/header.php
echo " " > ./pages/views/footer.php
