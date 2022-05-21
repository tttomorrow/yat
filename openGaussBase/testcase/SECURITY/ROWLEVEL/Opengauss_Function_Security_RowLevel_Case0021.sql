-- @testpoint: 修改行级访问控制
--step1: 创建用户；expect:成功
DROP USER IF EXISTS u01_security_RowLevel_0021;
DROP USER IF EXISTS u02_security_RowLevel_0021;
DROP USER IF EXISTS u03_security_RowLevel_0021;
CREATE USER u01_security_RowLevel_0021 PASSWORD 'Test@123';
CREATE USER u02_security_RowLevel_0021 PASSWORD 'Test@123';
CREATE USER u03_security_RowLevel_0021 PASSWORD 'Test@123';
--step2: 创建本地临时表，并给用户赋予访问权限；expect:成功
DROP TABLE IF EXISTS t_security_RowLwvel_0021;
CREATE TABLE t_security_RowLwvel_0021(id int, role varchar(100), data varchar(100));
GRANT SELECT ON t_security_RowLwvel_0021 TO u01_security_RowLevel_0021, u03_security_RowLevel_0021, u02_security_RowLevel_0021;
--step3: 创建行级访问策略；expect:成功
ALTER TABLE t_security_RowLwvel_0021 ENABLE ROW LEVEL SECURITY;
CREATE ROW LEVEL SECURITY POLICY rls_security_RowLwvel_0021 ON t_security_RowLwvel_0021 to u01_security_RowLevel_0021 USING(role = CURRENT_USER);
--step4: 修改行级访问策略；expect:成功
ALTER ROW LEVEL SECURITY POLICY rls_security_RowLwvel_0021 ON t_security_RowLwvel_0021 TO u01_security_RowLevel_0021, u03_security_RowLevel_0021;
ALTER ROW LEVEL SECURITY POLICY rls_security_RowLwvel_0021 ON t_security_RowLwvel_0021 RENAME TO rls_new_security_RowLwvel_0021;
ALTER ROW LEVEL SECURITY POLICY rls_new_security_RowLwvel_0021 ON t_security_RowLwvel_0021 USING (id > 2 AND role = current_user);
--step4: 清理环境；expect:成功
DROP TABLE IF EXISTS t_security_RowLwvel_0021 CASCADE;
DROP USER u01_security_RowLevel_0021 CASCADE;
DROP USER u02_security_RowLevel_0021 CASCADE;
DROP USER u03_security_RowLevel_0021 CASCADE;