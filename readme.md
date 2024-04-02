# Therma-sense

Therma-sense est une application de domotique permettant de connaitre la température de son logement. Elle se présente sous la forme d'une application web de type SAAS, reliée à un serveur qui communique, via protocole LORA, avec des capteurs de type Wyres STM Nucleo 401 

# Installation
## Back-end (serveur)

Le serveur est réalisé sous le framework Django en Python.
Il est composé d'une API REST, d'une base de données MariaDB et d'un module de communication LORA. Le serveur doit être de type Raspberry Pi4, adjoint d'un module Top Hat LoRa Node pHAT

https://learn.pi-supply.com/make/getting-started-with-the-raspberry-pi-lora-node-phat/
https://uk.pi-supply.com/products/iot-lora-node-phat-for-raspberry-pi

Pour executer ce programme, vous aurez besoin de pip et d'un serveur Mysql configué sur le port 3306.  
Créez un base de données, un utilisateur, et donnez lui les droits sur cette base.  
Ensuite modifiez le fichier **settings.py** pour ajouter le nom de votre base et votre utilisateur.

Puis chargez la base de données fourni avec le projet :
```
sudo mysql
CREATE DATABASE therma_sense;
CREATE USER 'username'@'hostname' IDENTIFIED BY 'password';
```
En remplaçant *username* par votre *login* et *password* par votre *mot de passe*.  
Puis reportez-les au sein de votre fichier **settings.py**

```
GRANT ALL PRIVILEGES ON therma_sense TO 'username'@'%';

mysqldump -u username -p therma_sense < therma_sense.sql
```

Puis, vous devez installer ces dépendances : 
```
pip install django-cors-headers
pip install pymysql
pip install python3-mysqldb
pip install djangorestframework-simplejwt
pip install django-crontab
sudo pip3 install rak811
```

Si vous avez un capteur LORA de disponible, placez la variable globale
*DISPOSE_LORA* à True au sein du fichier **settings.py**

Et pour lancer le programme, mettez vous à la racine du back end et faites :  
`python3 manage.py runserver`

## Front-end (application web)
L'application web est ecrite en Javascript ECMA6 natif et compilé avec Vite.

Pour executer le programme, vous avez besoin d'une version de nodeJS supérieure à la version 18.

Dans le fichier **parametres.js**, modifiez la variable *BACKEND_URL* en lui donnant l'adresse de votre serveur de back-end. Si vous n'avez pas fait de redirection via un serveur ou proxy, vous trouverez votre serveur à l'adresse http://127.0.0.1:8000

Puis faites une instalation: 
`npm install` et lancez l'application avec `npm run dev`
puis affichez la page au sein de votre navigateur web avec l'URL http://localhost:5173/

## Board
Pour installer le programme, il vous faut flasher votre board. A la racine du dossier board, faites :  
`make -j4 flash`
