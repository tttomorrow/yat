-- @testpoint: 插入非法空值，合理报错

drop table if exists integer08;
create table integer08 (id int,name integer);
insert into integer08 values (1,' ');
drop table integer08;