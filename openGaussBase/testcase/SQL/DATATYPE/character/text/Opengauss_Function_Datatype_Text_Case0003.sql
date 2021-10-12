-- @testpoint: 创建表，插入负值


drop table if exists test_text_03;
create table test_text_03(c_text text);
insert into test_text_03 values(-123456);
select * from test_text_03;
drop table test_text_03;