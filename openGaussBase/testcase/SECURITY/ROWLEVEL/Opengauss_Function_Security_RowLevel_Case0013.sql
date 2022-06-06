-- @testpoint: 支持hash表创建行级访问策略
--step1:  创建hash表；expect:成功
DROP TABLE IF EXISTS t_security_RowLwvel_0013;
CREATE TABLE t_security_RowLwvel_0013(id int, card integer NOT NULL,role char(5),data varchar(10)) PARTITION BY HASH (card)(PARTITION P1, PARTITION P2);
--step2: 创建行级访问策略；expect:成功
ALTER TABLE t_security_RowLwvel_0013 ENABLE ROW LEVEL SECURITY;
CREATE ROW LEVEL SECURITY POLICY rls_security_RowLwvel_0013 ON t_security_RowLwvel_0013 USING(role = CURRENT_USER);
--step4: 清理环境；expect:成功
DROP TABLE t_security_RowLwvel_0013 CASCADE;

