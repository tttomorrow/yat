-- @testpoint: 创建表单列不带名字的约束

--创建表单列不带名字的约束1
drop table if exists Persons;
create table Persons ( Id_P int not null, LastName varchar(255) not null, FirstName varchar(255),
address varchar(255), City varchar(255),check (Id_P>0) );

--创建表单列不带名字的约束2
drop table if exists Persons;
create table Persons ( Id_P int not null check (Id_P>0), LastName varchar(255) not null,
FirstName varchar(255), address varchar(255), City varchar(255) );
drop table Persons cascade;