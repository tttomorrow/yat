-- @testpoint: 将文本类型的值转换为指定格式的时间戳，insert插入数据时使用to_date函数

drop table if exists test2;
create table test2 (d date);
insert into test2 values(to_date('2018-01-15'));
drop table if exists test2;