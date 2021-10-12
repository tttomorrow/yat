-- @testpoint: 插入非法空值，合理报错

drop table if exists real_08;
create table real_08 (id int,name real);
insert into real_08 values (1,' ');
drop table real_08;