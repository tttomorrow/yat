-- @testpoint: 插入有效正整数

drop table if exists bigint01;
create table bigint01 (name bigint);
insert into bigint01 values (120);
insert into bigint01 values (99999999);
select * from bigint01;
drop table bigint01;