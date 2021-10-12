--  @testpoint:修改行访问控制策略表达式
--创建用户alice
drop user if exists alice cascade;
CREATE user alice PASSWORD 'Gauss@123';
--创建用户bob
drop user if exists bob cascade;
CREATE user bob PASSWORD 'Gauss@123';
--创建数据表all_data
drop table if exists all_data cascade;
CREATE TABLE all_data(id int, role varchar(100), data varchar(100));
--插入数据
INSERT INTO all_data VALUES(100, 'alice', 'alice data');
INSERT INTO all_data VALUES(200, 'bob', 'bob data');
INSERT INTO all_data VALUES(300, 'peter', 'peter data');
--创建行访问控制策略，当前用户只能查看用户自身的数据
drop ROW LEVEL SECURITY POLICY if exists all_data_rls ON all_data;
CREATE ROW LEVEL SECURITY POLICY all_data_rls ON all_data USING(role = CURRENT_USER);
--修改行访问控制策略表达式,分别指定用户为alice、public、alice and bob
ALTER ROW LEVEL SECURITY POLICY all_data_rls ON all_data to alice USING (id > 100 AND role = current_user);
ALTER ROW LEVEL SECURITY POLICY all_data_rls ON all_data to public USING (id > 200 AND role = current_user);
ALTER ROW LEVEL SECURITY POLICY all_data_rls ON all_data to alice,bob USING (id >= 200 AND role = current_user);
--删除行访问控制策略
drop ROW LEVEL SECURITY POLICY if exists all_data_rls ON all_data;
--删除表
drop table all_data cascade;
--删除用户
drop user alice cascade;
drop user bob cascade;