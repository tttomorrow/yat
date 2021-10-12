-- @testpoint: 插入正整数

drop table if exists real_01;
create table real_01 (name real);
insert into real_01 values (120);
insert into real_01 values (99999);
insert into real_01 values (1);
insert into real_01 values (2);
insert into real_01 values (3);
select * from real_01;
drop table real_01;