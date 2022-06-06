-- @testpoint: 不支持本地临时表定义行访问控制策略，合理报错
--step1: 创建本地临时表；expect:成功
DROP TABLE IF EXISTS t_security_RowLwvel_0015;
CREATE LOCAL TEMP TABLE t_security_RowLwvel_0015(id1 int,id2 int);
--step2: 创建行级访问策略；expect:失败
CREATE ROW LEVEL SECURITY POLICY rls_security_RowLwvel_0015 ON t_security_RowLwvel_0015 USING(role = CURRENT_USER);
--step4: 清理环境；expect:成功
DROP TABLE IF EXISTS t_security_RowLwvel_0015 CASCADE;