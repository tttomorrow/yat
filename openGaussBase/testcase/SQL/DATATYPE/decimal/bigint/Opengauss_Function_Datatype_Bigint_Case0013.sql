-- @testpoint: 插入非法空值，合理报错

drop table if exists bigint13;
create table bigint13 (id int,name bigint);
insert into bigint13 values (1,' ');
drop table bigint13;