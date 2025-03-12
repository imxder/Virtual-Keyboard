# Virtual Keyboard

Teclado Virtual para sites.

Este teclado gera os números em posições aleatórias, que variam a cada acesso do usuário. Mesmo que alguém consiga observar os botões utilizados pelo usuário, não será possível determinar a senha correta.

## Funcionalidades

- **Teclado Virtual**: Os botões com números são embaralhados a cada novo acesso, garantindo que a mesma senha inserida em diferentes acessos tenha sempre uma disposição diferente.
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

### Como rodar o projeto

1. Clone este repositório em sua máquina local:

    ```bash
    git clone https://github.com/seu_usuario/virtual-keyboard.git
    cd virtual-keyboard
    ```

2. Instale as dependências Python:

    Crie um ambiente virtual (opcional, mas recomendado):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Para Linux/macOS
    venv\Scripts\activate  # Para Windows
    ```

    Instale as dependências necessárias:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure o banco de dados MySQL:

    - Acesse o MySQL Workbench;
    
    - Crie o banco Users:

    ```sql
    create database users
    default character set utf8
    default collate utf8mb3_general_ci;
    ```
    - Crie a tabela usuario:

    ```sql
    create table usuario(
    id int not null auto_increment,
    user varchar(30) not null,
    senha varchar(255) not null,
    primary key(id)
    );
    ```
    - Adicione a coluna `ultimo_acesso` em usuario:

    ```sql
    alter table usuario add ultimo_acesso varchar(50);
    ```
    - Altere a tabela  usuario definindo um unico `user` para cada usuario, assim não havera outros com o mesmo user: 

    ```sql
    ALTER TABLE usuario ADD UNIQUE (user);
    ```

    - Crie um usuario na banco como teste:
    - 
    ```sql
    insert into usuario values(default, 'user', '1234');
    ```
  
    - Crie a tabela sessoes:

     ```sql
    CREATE TABLE Sessoes (
    hash VARCHAR(255) NOT NULL PRIMARY KEY,
    ordem VARCHAR(10) NOT NULL,
    disponivel BIT NOT NULL DEFAULT 1,
    ultima_vez_usado DATETIME NOT NULL
    );
    ```
    - Altera a coluna `orderm` em sessoes:
      
    ```sql
    ALTER TABLE sessoes MODIFY ordem VARCHAR(10);
    ```
4. Verifique o arquivo `servidor.py` para ver se a senha do banco está igual a da sua maquina.

5. Execute o arquivo `test.py` para gerar 10 sessões, pode executar varias vezes.

6. Execute o arquivo `app.py` para subir a API FLASK.

   - A aplicação estará acessível em `http://localhost:3308`. 

### Front-End

- **JavaScript**: A lógica do teclado virtual foi implementada em JavaScript, utilizando eventos de clique para capturar as teclas pressionadas.
- **CSS**: O design visual foi feito utilizando CSS, com a ajuda de flexbox e grid para criar um layout responsivo e agradável ao usuário.
