-- @testpoint: 插入不符合check项的值,合理报错
drop table if exists Persons;
create table Persons ( Id_P int not null check (Id_P>0), LastName varchar(255) not null,
FirstName varchar(255), address varchar(255), City varchar(255) );
insert into Persons values(0,'Mary','','','');
drop table Persons cascade;