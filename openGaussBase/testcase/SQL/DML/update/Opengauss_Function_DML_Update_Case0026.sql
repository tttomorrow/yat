-- @testpoint: 修改的表名不存在，合理报错
--建表
drop table if exists test_update002;
create table test_update002(c_integer integer, c_varchar varchar(50));
--插入数据
insert into test_update002 values(1,'aaaaa');
insert into test_update002 values(2,'bbbbb');
--修改数据,报错
update test_update002_new set c_varchar = 'new_a' where c_integer = 1;
--删表
drop table test_update002;