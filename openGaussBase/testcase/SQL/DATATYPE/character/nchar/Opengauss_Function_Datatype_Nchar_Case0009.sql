-- @testpoint: 插入值为汉字和英文

drop table if exists test_nchar_09;
create table test_nchar_09 (name nchar(20));
insert into test_nchar_09 values ('gkb中国');
insert into test_nchar_09 values ('中国gkb');
drop table test_nchar_09;