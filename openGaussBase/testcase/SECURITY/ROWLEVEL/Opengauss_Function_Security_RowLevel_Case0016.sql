-- @testpoint: 系统管理员不受行访问控制影响，可以查看表的全量数据
--step1: 创建表、用户；expect:成功
DROP USER IF EXISTS u01_security_RowLwvel_0016 CASCADE;
DROP USER IF EXISTS u02_security_RowLwvel_0016 CASCADE;
DROP USER IF EXISTS u03_security_RowLwvel_0016 CASCADE;
CREATE USER u01_security_RowLwvel_0016 PASSWORD 'Test@123';
CREATE USER u02_security_RowLwvel_0016 PASSWORD 'Test@123';
CREATE USER u03_security_RowLwvel_0016 PASSWORD 'Test@123';
DROP TABLE IF EXISTS t_security_RowLwvel_0016;
CREATE TABLE t_security_RowLwvel_0016(id int, role varchar(100), data varchar(100));
INSERT INTO t_security_RowLwvel_0016 VALUES(1, 'u01_security_RowLwvel_0016', 'alice data');
INSERT INTO t_security_RowLwvel_0016 VALUES(2, 'u02_security_RowLwvel_0016', 'bob data');
INSERT INTO t_security_RowLwvel_0016 VALUES(3, 'u03_security_RowLwvel_0016', 'peter data');
--step2: 创建行级访问策略；expect:失败
ALTER TABLE t_security_RowLwvel_0016 ENABLE ROW LEVEL SECURITY;
CREATE ROW LEVEL SECURITY POLICY rls_security_RowLwvel_0016 ON t_security_RowLwvel_0016 USING(role = CURRENT_USER);
--step3: 管理员永华查看表；expect:成功
select data from t_security_RowLwvel_0016 where role = 'u01_security_RowLwvel_0016';
select data from t_security_RowLwvel_0016 where role = 'u02_security_RowLwvel_0016';
select data from t_security_RowLwvel_0016 where role = 'u03_security_RowLwvel_0016';
--step4: 清理环境；expect:成功
DROP ROW LEVEL SECURITY POLICY rls_security_RowLwvel_0016 ON t_security_RowLwvel_0016;
DROP TABLE t_security_RowLwvel_0016 CASCADE;
DROP USER u01_security_RowLwvel_0016 CASCADE;
DROP USER u02_security_RowLwvel_0016 CASCADE;
DROP USER u03_security_RowLwvel_0016 CASCADE;