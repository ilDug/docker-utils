#!bash

echo "inizializzazione del progetto NPM\n\n\n"

# npm 
npm init

# FONTAWESOME TOKEN
echo "@fortawesome:registry=https://npm.fontawesome.com/
//npm.fontawesome.com/:_authToken=4A5F644E-0CEE-455A-BE26-AAECCDE19886" > ./.npmrc

# CORE PACKAGES
npm install  \
    lodash \
    @fortawesome/fontawesome-pro \
    animate.css \
    bootstrap \
    rxjs \
    @popperjs/core \
    js-cookie


# DEV DEPENDENCIES
npm install --save-dev \
    typescript \
    webpack webpack-cli \
    ts-loader \
    style-loader sass-loader node-sass mini-css-extract-plugin css-loader \
    file-loader copy-webpack-plugin clean-webpack-plugin \
    @types/bootstrap


cat <<EOF
#############################
ATTENZIONE
#############################

Aggiungere le seguenti righe nella sezione SCRIPTS del file package.json

    "dev": "webpack --progress --watch --config webpack.config.js --mode=development",
    "build": "webpack  --config  webpack.config.js --mode=production"

####################################################################
EOF
