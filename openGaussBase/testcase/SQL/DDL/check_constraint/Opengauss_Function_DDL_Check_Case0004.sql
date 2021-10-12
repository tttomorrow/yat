-- @testpoint: 创建重复约束，合理报错
drop table if exists Persons;
create table Persons ( Id_P int not null check (Id_P>0), LastName varchar(255) not null,
 FirstName varchar(255), address varchar(255), City varchar(255),check (Id_P<0) );
insert into Persons values('','Mary','','','');
drop table Persons cascade;