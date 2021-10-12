-- @testpoint: 插入字符串类型整数

drop table if exists bigint04;
create table bigint04 (name bigint);
insert into bigint04 values ('123');
select * from bigint04;
drop table bigint04;
