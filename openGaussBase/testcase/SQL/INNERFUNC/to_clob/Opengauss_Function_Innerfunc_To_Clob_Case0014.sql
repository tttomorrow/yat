-- @testpoint:  创建索引时使用to_clob类型转换函数

drop table if exists test2;
drop index if exists test1_index;
create table test2(riqi int);
insert into test2 values(10);
create index test1_index on test2(riqi);
select * from test2 where riqi<to_clob(12);
drop index if exists test1_index;
drop table if exists test2;