-- @testpoint: 插入特殊字符
-- @modify at: 2020-11-05

drop table if exists test_character_13;
create table test_character_13 (name character(20));
insert into test_character_13 values ('$@#%……&*（)');
select * from test_character_13;
drop table test_character_13;