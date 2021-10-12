-- @testpoint: 插入非法空值，合理报错

drop table if exists smallint13;
create table smallint13 (id int,name smallint);
insert into smallint13 values (1,' ');
drop table smallint13;