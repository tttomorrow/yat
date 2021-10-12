-- @testpoint: 类型转换函数to_timestamp，作为参数插入到数据表

drop table if exists test2;
create table test2 (d timestamp);
insert into test2 values(to_timestamp('2018-01-15','yyyy-mm-dd'));
drop table if exists test2;