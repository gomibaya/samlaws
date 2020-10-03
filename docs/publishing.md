# publishing.md

Se va a trabajar con varios repositorios

 1) Publicación en github - Nombre: github
 2) Publicación en git privado - Nombre: private
 3) Otros posibles

Forma normal seria:

git remote add origin https://github.com/gomibaya/[nombreproyecto].git


Forma en varios repositorios(git ya existent):

1) git remote set-url --add --push all https://github.com/gomibaya/[nombreproyecto].git
2) --private--


Forma correcta:

 1)
 - git remote add origin https://github.com/gomibaya/[nombreproyecto].git 

 2)
 - git remote add private --private--


Para adaptarlo a utilizar multiple accounts, utilizar el método de set-url para modificarlo, por ejemplo:
git remote set-url origin git@github.com-gomibaya:gomibaya/[nombreproyecto].git


Refs:
 - https://jigarius.com/blog/multiple-git-remote-repositories
 - https://www.freecodecamp.org/news/manage-multiple-github-accounts-the-ssh-way-2dadc30ccaca/
