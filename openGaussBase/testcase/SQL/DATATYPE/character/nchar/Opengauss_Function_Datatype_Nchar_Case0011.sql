-- @testpoint: 插入超出范围正常值，默认字节长度，合理报错
-- @modified at: 2020-11-16

drop table if exists test_nchar_11;
create table test_nchar_11 (name nchar);
insert into test_nchar_11 values ('aa');
drop table test_nchar_11;
