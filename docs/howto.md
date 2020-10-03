# howto.md

La construcción se basará en entornos:
 - Debian Buster 10
 - Debian Bullseye 11 (No validada hasta que sea estable)
 - Ubuntu 20.04 LTS

Soporte sólo python3, tanto en aplicación, como en build

Como root

pip3 install virtualenv

# Como admin, o user, si no se quiere que se aplique a todo el equipo
pip3 install tox
pip3 install pylama
