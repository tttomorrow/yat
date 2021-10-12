-- @testpoint: 创建列类型为字符类型VARCHAR2(n)的表

drop table if exists table_1;
create table table_1(a VARCHAR2(10));
insert into table_1 values('张无忌');
insert into table_1 values('赵敏张无忌'::varchar(6));
select * from table_1;
drop table if exists table_1;
