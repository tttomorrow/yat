-- @testpoint: 插入合理字符串，默认字节长度
-- @modify at: 2020-11-05


drop table if exists test_char_11;
create table test_char_11 (name char);
insert into test_char_11 values ('a');
select * from test_char_11;
drop table test_char_11;