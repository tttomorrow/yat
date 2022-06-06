-- @testpoint: 支持unlogged表创建行级访问策略
--step1: 创建unlogged表；expect:成功
DROP TABLE IF EXISTS t_security_RowLwvel_0012;
CREATE UNLOGGED TABLE t_security_RowLwvel_0012(id int, role char(5), data varchar(10));
--step2: 创建行级访问策略；expect:成功
ALTER TABLE t_security_RowLwvel_0012 ENABLE ROW LEVEL SECURITY;
CREATE ROW LEVEL SECURITY POLICY rls_security_RowLwvel_0012 ON t_security_RowLwvel_0012 USING(role = CURRENT_USER);
--step3: 清理环境；expect:成功
DROP TABLE t_security_RowLwvel_0012 CASCADE;