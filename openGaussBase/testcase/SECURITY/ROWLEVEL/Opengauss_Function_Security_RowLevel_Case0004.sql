-- @testpoint: 不同的数据表，可以有同名的行访问控制策略
--step1: 创建表；expect:成功
DROP TABLE IF EXISTS t01_security_RowLwvel_0004;
DROP TABLE IF EXISTS t02_security_RowLwvel_0004;
CREATE TABLE t01_security_RowLwvel_0004(id int, role varchar(10), data varchar(10));
CREATE TABLE t02_security_RowLwvel_0004(id int, role varchar(10), data varchar(10));
--step2: 创建行级访问策略；expect:成功
ALTER TABLE t01_security_RowLwvel_0004 ENABLE ROW LEVEL SECURITY;
ALTER TABLE t02_security_RowLwvel_0004 ENABLE ROW LEVEL SECURITY;
CREATE ROW LEVEL SECURITY POLICY rls_security_RowLwvel_0004 ON t01_security_RowLwvel_0004 USING(role = CURRENT_USER);
CREATE ROW LEVEL SECURITY POLICY rls_security_RowLwvel_0004 ON t02_security_RowLwvel_0004 USING(role = CURRENT_USER);
--step3: 清理环境；expect:成功
DROP TABLE t01_security_RowLwvel_0004 CASCADE;
DROP TABLE t02_security_RowLwvel_0004 CASCADE;