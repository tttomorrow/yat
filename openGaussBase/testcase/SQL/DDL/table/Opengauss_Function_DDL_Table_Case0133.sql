-- @testpoint: 创建列类型为特殊字符类型“char”的表,插入非字符类型时合理报错
drop table if exists table_2;
create table table_2(a "char");
insert into table_2 values('qwweerth');
insert into table_2 values(122);
select * from table_2;
drop table if exists table_2;