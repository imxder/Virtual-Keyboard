# Virtual Keyboard

Teclado Virtual para sites.

Este teclado gera os números em posições aleatórias, que variam a cada acesso do usuário. Mesmo que alguém consiga observar os botões utilizados pelo usuário, não será possível determinar a senha correta.

## Funcionalidades

- **Teclado Virtual Aleatório**: Os botões com números são embaralhados a cada novo acesso, garantindo que a mesma senha inserida em diferentes acessos tenha sempre uma disposição diferente.
- **Segurança de Senha**: Ao usar o teclado virtual, a senha do usuário nunca fica visível em sua forma completa, dificultando a captura por programas de "keylogging" ou observação.
- **Login Seguro**: Utilização do algoritmo de hash `bcrypt` para garantir a segurança das senhas armazenadas.
- **Interface Amigável**: A interface do teclado é simples e intuitiva, permitindo que o usuário faça login com facilidade, mesmo em ambientes públicos.

## Arquitetura e Stack

### Detalhes da Stack e Integrações:

- **Implementação em Python 3.13.2: Linguagem de programação amplamente utilizada em aplicações web, desenvolvimento de software, ciência de dados e machine learning (ML).
- **Uso do framework Flask**: Framework web para Python, utilizado neste projeto principalmente para criação de rotas entre as páginas.
- **Persistência de dados em MySQL**: Banco de dados utilizado para armazenar dados de usuários, com a biblioteca `mysql-connector-python` para integração.
- **Uso do algoritmo bcrypt**: Algoritmo de hash e criptografia utilizado para segurança das senhas. Implementado com a biblioteca `bcrypt`.
- **Uso do MySQL Workbench**: Ferramenta para a criação e alterações no banco de dados MySQL, proporcionando uma interface visual para gestão de banco de dados.
- **Teclado Virtual em JavaScript**: Implementação de um teclado virtual interativo em JavaScript, com a geração dinâmica de números em posições aleatórias.
- **HTML/CSS para Front-End**: Interface do usuário desenvolvida em HTML5 e estilizada com CSS, criando uma experiência visual limpa e funcional.


### Pré-requisitos

Antes de rodar o projeto, você precisa ter os seguintes itens instalados:

- **Python 3.13.2 
- **MySQL Server** (com o banco de dados configurado)
- **MySQL Workbench** (opcional, mas recomendado para gerenciar o banco de dados visualmente)


### Front-End

- **JavaScript**: A lógica do teclado virtual foi implementada em JavaScript, utilizando eventos de clique para capturar as teclas pressionadas.
- **CSS**: O design visual foi feito utilizando CSS, com a ajuda de flexbox e grid para criar um layout responsivo e agradável ao usuário.
