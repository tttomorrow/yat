--  @testpoint:openGauss关键字savepoint(非保留),使用ROLLBACK TO 
--清理环境，删除表格
 DROP TABLE if exists table1;

--创建一个新表。
CREATE TABLE table1(a int); 
--开启事务。
START TRANSACTION; 
--插入数据。 
INSERT INTO table1 VALUES (1); 
--建立保存点。  
SAVEPOINT my_savepoint; 
--插入数据。 
INSERT INTO table1 VALUES (2); 
--回滚保存点。 
ROLLBACK TO SAVEPOINT my_savepoint; 
--插入数据。 
INSERT INTO table1 VALUES (3); 
--提交事务。 
COMMIT; 
--查询表的内容，会同时看到1和3,不能看到2，因为2被回滚。 postgres=# 
SELECT * FROM table1; 
--删除表。 
DROP TABLE table1; 

