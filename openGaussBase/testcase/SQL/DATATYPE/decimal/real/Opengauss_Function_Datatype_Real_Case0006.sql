-- @testpoint: 插入bool类型，合理报错

drop table if exists real_06;
create table real_06 (name real);
insert into real_06 values (false);
insert into real_06 values (true);
drop table real_06;