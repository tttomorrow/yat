--  @testpoint:插入字符串类型
drop table if exists bigint10;
create table bigint10 (name bigint);
insert into bigint10 values ('12345678');
select * from bigint10;
-----插入非整数字符，应该报错
insert into bigint10 values ('111a222');
drop table if exists bigint10;