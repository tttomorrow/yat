--  @testpoint:视图定义行访问控制策略，合理报错
--建表
drop table if exists test_policy cascade;
create table test_policy(id int,usr varchar(20));
--插入数据
insert into test_policy(id, usr) values(1, 'user1');
insert into test_policy(id, usr) values(2, 'user2');
insert into test_policy(id, usr) values(3, 'user2');
insert into test_policy(id, usr) values(4, 'user2');
insert into test_policy(id, usr) values(5, 'user1');
insert into test_policy(id, usr) values(5, 'user3');
--创建视图
CREATE or replace VIEW test_policy_view AS SELECT * FROM test_policy WHERE id > 2;
--给视图创建行访问控制策略，合理报错ERROR:  "test_policy_view" is not a normal table
drop POLICY if exists test_pol ON test_policy_view;
CREATE POLICY test_pol ON test_policy_view FOR update TO PUBLIC USING (usr = current_user);
--删除表
drop table test_policy cascade;
