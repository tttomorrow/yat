-- @testpoint: openGauss保留关键字current_catalog作为触发器名，部分测试点合理报错
--前提条件
--创建源表
drop table if exists test_trigger_src_tbl;
CREATE TABLE test_trigger_src_tbl(id1 INT, id2 INT, id3 INT);

--创建触发表
drop table if exists test_trigger_des_tbl;
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
CREATE TRIGGER current_catalog
           BEFORE INSERT ON test_trigger_src_tbl
           FOR EACH ROW
           EXECUTE PROCEDURE tri_insert_func();
		   /
		   
--加双引号，创建成功
CREATE TRIGGER "current_catalog"
           BEFORE INSERT ON test_trigger_src_tbl
           FOR EACH ROW
           EXECUTE PROCEDURE tri_insert_func();
		   /
		   
--清理环境		   
drop TRIGGER "current_catalog" on test_trigger_src_tbl cascade;

--加单引号，合理报错
CREATE TRIGGER 'current_catalog'
           BEFORE INSERT ON test_trigger_src_tbl
           FOR EACH ROW
           EXECUTE PROCEDURE tri_insert_func();
		   /
		   
--带反引号，合理报错
CREATE TRIGGER `current_catalog`
           BEFORE INSERT ON test_trigger_src_tbl
           FOR EACH ROW
           EXECUTE PROCEDURE tri_insert_func();
		   /
drop table if exists test_trigger_src_tbl;
drop table if exists test_trigger_des_tbl;
drop table if exists tri_insert_func;