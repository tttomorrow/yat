-- @testpoint: 创建列类型为字符类型NVARCHAR2(n)的表
drop table if exists table_1;
create table table_1(a NVARCHAR2(10));
insert into  table_1 values ('张三');
insert into  table_1 values ('qazw');
insert into  table_1 values (123456677);
select * from table_1;
drop table if exists table_1;
