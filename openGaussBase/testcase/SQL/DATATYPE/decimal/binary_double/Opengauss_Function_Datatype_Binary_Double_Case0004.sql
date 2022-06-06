-- @testpoint: 插入字符串形式小数

drop table if exists binary_double04;
create table binary_double04 (name binary_double);
insert into binary_double04 values ('14165132.11111111111111111111111111111111111');
insert into binary_double04 values ('0.0000023');
insert into binary_double04 values ('-99999999.3653');
insert into binary_double04 values ('-0.00000232222');
select * from binary_double04;
drop table binary_double04;
