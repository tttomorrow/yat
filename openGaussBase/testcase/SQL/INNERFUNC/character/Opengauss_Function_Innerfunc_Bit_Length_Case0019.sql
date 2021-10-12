-- @testpoint: 未插入数据

drop table if exists test_char_003;
create table test_char_003 (name char(18));
select bit_length(name) from test_char_003;
DROP TABLE IF EXISTS test_char_003;