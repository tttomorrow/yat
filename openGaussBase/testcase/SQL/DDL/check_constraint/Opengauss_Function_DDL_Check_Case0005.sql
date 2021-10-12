-- @testpoint: alter单条件约束
drop table if exists Persons;
create table Persons ( Id_P int not null, LastName varchar(255) not null,
FirstName varchar(255), address varchar(255), City varchar(255) );
alter table Persons add check (Id_P>0);
drop table Persons cascade;