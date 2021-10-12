-- @testpoint: 创建表，插入布尔类型值


drop table if exists test_text_05;
create table test_text_05(id int,c_text text);
insert into test_text_05 values(1,true);
insert into test_text_05 values(1,false);
select * from test_text_05;
drop table test_text_05;