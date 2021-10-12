-- @testpoint: 参数default_transaction_read_only保持默认，执行DMl操作，成功
--查看默认值
show default_transaction_read_only;
--建表
drop table if exists test_isolation067;
create table test_isolation067(id int,name varchar(20));
--插入数据
insert into test_isolation067 values(1,'tom'),(2,'lily');
--修改
update test_isolation067 set id = id+1;
--查询
select * from test_isolation067;
--删除
delete from test_isolation067;
--删表
drop table test_isolation067;