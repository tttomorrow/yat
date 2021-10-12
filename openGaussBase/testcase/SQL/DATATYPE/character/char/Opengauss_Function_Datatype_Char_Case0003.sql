-- @testpoint: 插入正常值，字节长度设定为1
-- @modify at: 2020-11-05

drop table if exists test_char_03;
create table test_char_03 (name char(1));
insert into test_char_03 values ('a');
select * from test_char_03;
drop table test_char_03;
