-- @testpoint: 边界值为18测试

drop table if exists test_char_003;
create table test_char_003 (name char(18));
insert into test_char_003 values ('中aA$@#%.&*（）');
select bit_length(name) from test_char_003;
DROP TABLE IF EXISTS test_char_003;