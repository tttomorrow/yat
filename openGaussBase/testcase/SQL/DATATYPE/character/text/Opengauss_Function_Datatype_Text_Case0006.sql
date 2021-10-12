-- @testpoint: 插入汉字和英文

drop table if exists test_text_06;
create table test_text_06(c_text text);
insert into test_text_06 values('测试数据库abc');
insert into test_text_06 values('abcdfdf测试数据库');
select * from test_text_06;
drop table test_text_06;