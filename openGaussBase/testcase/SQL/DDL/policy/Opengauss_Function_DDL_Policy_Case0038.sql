--  @testpoint:删除行访问控制策略，添加 CASCADE | RESTRICT 选项
--创建数据表all_data
drop table if exists all_data cascade;
CREATE TABLE all_data(id int, role varchar(100), data varchar(100));
--创建行访问控制策略
drop ROW LEVEL SECURITY POLICY if exists all_data_rls ON all_data;
CREATE ROW LEVEL SECURITY POLICY all_data_rls ON all_data USING(role = CURRENT_USER);
--删除行访问控制策略,添加cascade，删除成功，资料表示CASCADE/RESTRICT仅适配此语法，无对象依赖于该行访问控制策略，CASCADE和RESTRICT效果相同
DROP ROW LEVEL SECURITY POLICY all_data_rls ON all_data cascade;
--删除不存在的行访问控制策略,添加if exists和RESTRICT
DROP ROW LEVEL SECURITY POLICY if exists all_data_rls ON all_data RESTRICT;
--创建行访问控制策略
drop ROW LEVEL SECURITY POLICY if exists all_data_rls1 ON all_data;
CREATE ROW LEVEL SECURITY POLICY all_data_rls1 ON all_data USING(role = CURRENT_USER);
--删除表
drop table all_data cascade;
--删除行访问控制策略all_data_rls1，表已不存在，故策略删除报错
drop ROW LEVEL SECURITY POLICY all_data_rls1 ON all_data RESTRICT;