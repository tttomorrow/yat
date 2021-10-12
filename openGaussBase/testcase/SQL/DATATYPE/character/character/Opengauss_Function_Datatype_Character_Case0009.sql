-- @testpoint: 插入值为汉字和英文混合


drop table if exists test_character_09;
create table test_character_09 (name character(20));
insert into test_character_09 values ('gkb中国');
insert into test_character_09 values ('中国gkb');
drop table test_character_09;