--  @testpoint:插入字符串类型整数
drop table if exists bigint04;
create table bigint04 (name bigint);
insert into bigint04 values ('14165132');
select * from bigint04;
drop table if exists bigint04;