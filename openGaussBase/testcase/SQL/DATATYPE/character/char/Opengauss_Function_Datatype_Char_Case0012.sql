-- @testpoint: 插入超出默认字节长度值，合理报错
-- @modify at: 2020-11-05


drop table if exists test_char_12;
create table test_char_12 (name char);
insert into test_char_12 values ('aa');
select * from test_char_12;
drop table test_char_12;
