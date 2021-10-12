-- @testpoint: 不设定n大小值，默认为1，插入正常字符
drop table if exists test_char_11;
create table test_char_11 (name char);
insert into test_char_11 values ('a');
select bit_length(name) from test_char_11;
DROP TABLE IF EXISTS test_char_11;