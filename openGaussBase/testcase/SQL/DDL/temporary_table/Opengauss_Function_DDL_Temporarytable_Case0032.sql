-- @testpoint: 创建临时表的外键约束，引用普通表，合理报错
-- @modify at: 2020-11-24
--建表1
drop table if exists table_032;
create table table_032
(
 id int not null ,
 primary key (id)
);
--建表2
drop table if exists table_032_bak;
create table table_032_bak(
id_number int not null ,
primary key(id_number)
);
--创建临时表，报错
drop table if exists temp_table_032;
create temporary table temp_table_032(
id_number int not null,
cloth_id int references table_032_bak(id_number),
user_id int references table_032(id)
);
--删表
drop table table_032;
drop table table_032_bak;
