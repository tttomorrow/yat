-- @testpoint: openGauss保留关键字having作为触发器名，部分测试点合理报错
--前提条件
--创建源表
DROP TABLE IF EXISTS test_trigger_src_tbl;
CREATE TABLE test_trigger_src_tbl(id1 INT, id2 INT, id3 INT);

--创建触发表
DROP TABLE IF EXISTS test_trigger_des_tbl;
CREATE TABLE test_trigger_des_tbl(id1 INT, id2 INT, id3 INT);

--创建触发器函数
 CREATE OR REPLACE FUNCTION tri_insert_func() RETURNS TRIGGER AS
           $$
           DECLARE
           BEGIN
                   INSERT INTO test_trigger_des_tbl VALUES(NEW.id1, NEW.id2, NEW.id3);
                   RETURN NEW;
           END
           $$ LANGUAGE PLPGSQL;
           /

 --不带引号，合理报错
CREATE TRIGGER having
           BEFORE INSERT ON test_trigger_src_tbl
           FOR EACH ROW
           EXECUTE PROCEDURE tri_insert_func();
		   /
		   
--加双引号，创建成功
CREATE TRIGGER "having"
           BEFORE INSERT ON test_trigger_src_tbl
           FOR EACH ROW
           EXECUTE PROCEDURE tri_insert_func();
		   /
		   
--清理环境		   
DROP TRIGGER "having" ON test_trigger_src_tbl CASCADE;

--加单引号，合理报错
CREATE TRIGGER 'having'
           BEFORE INSERT ON test_trigger_src_tbl
           FOR EACH ROW
           EXECUTE PROCEDURE tri_insert_func();
		   /
		   
--带反引号，合理报错
CREATE TRIGGER `having`
           BEFORE INSERT ON test_trigger_src_tbl
           FOR EACH ROW
           EXECUTE PROCEDURE tri_insert_func();
		   /

--清理环境
DROP FUNCTION tri_insert_func;
DROP TABLE IF EXISTS test_trigger_src_tbl;
DROP TABLE IF EXISTS test_trigger_des_tbl;