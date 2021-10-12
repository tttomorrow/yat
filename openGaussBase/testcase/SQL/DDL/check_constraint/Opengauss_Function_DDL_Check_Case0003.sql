-- @testpoint: 同字段创建唯一、check约束
drop table if exists Persons;
create table Persons ( Id_P int not null unique check (Id_P>0), LastName varchar(255) not null,
FirstName varchar(255), address varchar(255), City varchar(255) );
drop table Persons cascade;