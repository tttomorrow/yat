--  @testpoint:创建表并指定其中一列是主键且给主键列取默认值
--预置条件enable_upsert_to_merge为off
drop  table if exists t02;
--col1 列为主键且默认值是1
CREATE TABLE t02 (col1 INT DEFAULT 1 PRIMARY KEY, col2 INT, col3 INT);
--使用insert..update语句，插入一条数据(1, 2, 3)
INSERT INTO t02 VALUES(1, 2, 3) ON DUPLICATE KEY UPDATE col2 = 20;
SELECT * FROM t02;
--使用insert..update语句,修改原数据(1, 2, 3)为(1, 20, 3)
INSERT INTO t02 VALUES(1, 20, 3) ON DUPLICATE KEY UPDATE col2 = 20;
--按col2列排序
SELECT * FROM t02 ORDER BY 2;
--使用insert..update语句，给col1不插入值，数据(1, 20, 3)更改为(1,25,3)
INSERT INTO t02(col2,col3) VALUES(2, 3) ON DUPLICATE KEY UPDATE col2 = 25;
SELECT * FROM t02 ORDER BY 1;
drop table t02;