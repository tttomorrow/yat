-- @testpoint: 插入正常值
-- @modify at: 2020-11-05

drop table if exists test_character_02;
create table test_character_02 (name character(20));
insert into test_character_02 values ('abcdefgh');
insert into test_character_02 values ('测试');
insert into test_character_02 values (123);
select * from test_character_02;
drop table test_character_02;
