-- @testpoint: 插入空值
-- @modify at: 2020-11-05


drop table if exists test_character_07;
create table test_character_07 (id int,name character(8));
insert into test_character_07 values (1,'');
insert into test_character_07 values (1,null);
drop table test_character_07;