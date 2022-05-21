-- @testpoint: 支持列存表行级访问策略
--step1: 创建列存表；expect:成功
DROP TABLE IF EXISTS t_security_RowLwvel_0010;
CREATE TABLE t_security_RowLwvel_0010(id int, role varchar(10), data varchar(10)) WITH (ORIENTATION = COLUMN);
--step2: 创建行级访问策略；expect:成功
ALTER TABLE t_security_RowLwvel_0010 ENABLE ROW LEVEL SECURITY;
CREATE ROW LEVEL SECURITY POLICY rls_security_RowLwvel_0010 ON t_security_RowLwvel_0010 USING(role = CURRENT_USER);
--step3: 清理环境；expect:成功
DROP TABLE t_security_RowLwvel_0010 CASCADE;