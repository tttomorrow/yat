--  @testpoint:openGauss关键字savepoint(非保留),使用RELEASE SAVEPOINT删除一个保存点，但是保留该保存点建立后执行的命令的效果
--清理环境，删除表格
 DROP TABLE if exists table2;
--创建一个新表。
 CREATE TABLE table2(a int);
--开启事务。
start  TRANSACTION;
 --插入数据。
 INSERT INTO table2 VALUES (3);
 --建立保存点。
 SAVEPOINT my_savepoint;
 --插入数据。
 INSERT INTO table2 VALUES (4);
 --回滚保存点。
 RELEASE SAVEPOINT my_savepoint;
 --提交事务。
 COMMIT;
 --查询表的内容，会同时看到3和4。
 SELECT * FROM table2;
 --删除表。
 DROP TABLE table2;
