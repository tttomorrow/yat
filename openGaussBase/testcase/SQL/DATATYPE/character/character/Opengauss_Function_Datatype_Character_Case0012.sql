-- @testpoint: 插入正常值，超出字节长度默认值，合理报错
-- @modify at: 2020-11-05

drop table if exists test_character_12;
create table test_character_12 (name character);
insert into test_character_12 values ('aa');
drop table test_character_12;