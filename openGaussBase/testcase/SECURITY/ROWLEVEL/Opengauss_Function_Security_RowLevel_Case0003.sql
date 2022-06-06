-- @testpoint: 同一个数据表上不能有同名的行访问控制策略,合理报错
--step1: 创建表；expect:成功
DROP TABLE IF EXISTS t_security_RowLwvel_0003;
CREATE TABLE t_security_RowLwvel_0003(id int, role varchar(10), data varchar(10));
INSERT INTO t_security_RowLwvel_0003 VALUES(1, 'alice', 'alice data');
INSERT INTO t_security_RowLwvel_0003 VALUES(2, 'bob', 'bob data');
INSERT INTO t_security_RowLwvel_0003 VALUES(3, 'peter', 'peter data');
--step2: 同一个数据表上创建同名的行访问控制策略；expect:合理报错
ALTER TABLE t_security_RowLwvel_0003 ENABLE ROW LEVEL SECURITY;
CREATE ROW LEVEL SECURITY POLICY rls_security_RowLwvel_0003 ON t_security_RowLwvel_0003 USING(role = CURRENT_USER);
CREATE ROW LEVEL SECURITY POLICY rls_security_RowLwvel_0003 ON t_security_RowLwvel_0003 USING(role = CURRENT_USER);
--step3: 清理环境；expect:成功
DROP TABLE t_security_RowLwvel_0003 CASCADE;