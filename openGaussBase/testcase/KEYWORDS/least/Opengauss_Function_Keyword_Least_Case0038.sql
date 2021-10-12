--  @testpoint:定义列的数据类型是least，应该报错
drop table if exists test;
create table test (id least);