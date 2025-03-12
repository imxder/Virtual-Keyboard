
create database users
default character set utf8
default collate utf8mb3_general_ci;
 
create table usuario(
id int not null auto_increment,
user varchar(30) not null,
senha varchar(255) not null,
primary key(id)
 
)default charset = utf8;
 
drop table usuario;
 
 
insert into usuario values(default, 'alex', '1234');
 
select * from usuario;
select * from sessoes where disponivel=1;

select * from sessoes;
 
SELECT hash, ordem FROM sessoes WHERE disponivel = 1 ORDER BY ultima_vez_usado ASC
 
DELETE FROM usuario WHERE id IN (1, 2, 3, 4, 5, 6, 7, 8, 9);

DESC sessoes; 
ALTER TABLE sessoes MODIFY ordem VARCHAR(10);

ALTER TABLE usuario
ADD UNIQUE (user);
 
alter table usuario add ultimo_acesso varchar(50);
 
 
CREATE TABLE Sessoes (
  hash VARCHAR(255) NOT NULL PRIMARY KEY,
  ordem INT NOT NULL,
  disponivel BIT NOT NULL DEFAULT 1,
  ultima_vez_usado DATETIME NOT NULL
);