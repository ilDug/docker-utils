#!bash

# composer
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php composer-setup.php
php -r "unlink('composer-setup.php');"

echo "inizializzazione della configurazione di COMPSER"
echo "servono lacune infomazione per i NAMESPACE di PHP"
echo "i namespace saranno nella forme NOMESITO\PROGETTO"
echo "inserire il valore per NOMESITO [ ad es. posterbook]"
read name_of_site
echo "inserire il valore per PROGETTO [ad es. web]"
read name_of_project
echo "inizializzazione in corso"
php composer.phar init  --name="$name_of_site"/"$name_of_project"  \
  --description="dag website"  \
  --author="DagTech <marco.dognini@dagtech.it>"  \
  --type="project"  \
  --require="phpmailer/phpmailer:^6.5"   \
  --require="bramus/router:^1.6"   \
  --require="lcobucci/jwt:^4.1"   \
  --require="ildug/php-utils:^1.0" \
  --autoload="lib/php/" 
