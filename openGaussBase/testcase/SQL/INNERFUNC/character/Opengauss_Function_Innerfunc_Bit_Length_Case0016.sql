-- @testpoint: 最小值1测试
drop table if exists test_char_003;
create table test_char_003 (name char(1));
insert into test_char_003 values ('a');
select bit_length(name) from test_char_003;
DROP TABLE IF EXISTS test_char_003;