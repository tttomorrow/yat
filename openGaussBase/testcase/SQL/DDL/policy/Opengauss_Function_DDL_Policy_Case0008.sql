--  @testpoint:创建行访问控制策略，参数policy_name测试
--创建用户alice
drop user if exists alice cascade;
CREATE user alice PASSWORD 'Gauss@123';
--创建用户bob
drop user if exists bob cascade;
CREATE user bob PASSWORD 'Gauss@123';
--创建行存表all_data
drop table if exists all_data;
CREATE TABLE all_data(id int, role varchar(100), data varchar(100)) with (ORIENTATION = ROW);
--向表插入数据
INSERT INTO all_data VALUES(1, 'alice', 'alice data');
INSERT INTO all_data VALUES(2, 'bob', 'bob data');
INSERT INTO all_data VALUES(3, 'peter', 'peter data');
--将表all_data的读取权限赋予alice和bob用户
GRANT SELECT ON all_data TO alice, bob;
--打开行访问控制策略开关
ALTER TABLE all_data ENABLE ROW LEVEL SECURITY;
--创建行访问控制策略，行访问控制策略名称不存在，当前用户只能查看用户自身的数据
drop POLICY if exists all_data_rls ON all_data cascade;
CREATE ROW LEVEL SECURITY POLICY all_data_rls ON all_data USING(role = CURRENT_USER);
--同一个数据表上创建相同行访问控制策略名称,合理报错
CREATE ROW LEVEL SECURITY POLICY all_data_rls ON all_data USING(role = CURRENT_USER);
--删除行访问控制策略
drop POLICY if exists all_data_rls ON all_data cascade;
--删除表
drop table all_data;
--删除用户
drop user alice cascade;
drop user bob cascade;