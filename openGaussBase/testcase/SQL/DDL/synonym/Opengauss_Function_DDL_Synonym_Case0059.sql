-- @testpoint: 删除同义词，同义词不存在，省略if exists 选项，合理报错
-- @modify at: 2020-11-26
--建表
drop table if exists test_SYN_056;
create table test_SYN_056(a int);
--创建同义词
drop synonym if exists test_SYN_056bak;
create synonym test_SYN_056bak for test_SYN_056;
--删除存在的同义词
drop synonym test_SYN_056bak;
--删除的同义词不存在，不会报错
drop synonym if exists test_SYN_056bak;
--删除同义词不存在，报错
drop synonym test_SYN_056bak;
--删表
drop table test_SYN_056;