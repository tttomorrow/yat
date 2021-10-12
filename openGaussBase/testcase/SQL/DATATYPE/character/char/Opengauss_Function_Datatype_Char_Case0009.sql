-- @testpoint: 插入空值
-- @modify at: 2020-11-05

drop table if exists test_char_09;
create table test_char_09 (name char(5));
insert into test_char_09 values ('');
select * from test_char_09;
drop table test_char_09;