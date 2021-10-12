-- @testpoint: opengauss关键字Header(非保留)，作为触发器名，部分测试点合理报错

--前置条件
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

--关键字explain作为作为触发器名，不带引号，创建成功
--创建INSERT触发器不带引号，创建成功
CREATE TRIGGER Header BEFORE INSERT ON test_trigger_src_tbl FOR EACH ROW EXECUTE PROCEDURE tri_insert_func();
/
DROP TRIGGER Header ON test_trigger_src_tbl CASCADE;

--关键字explain作为触发器名，加双引号，创建成功
--创建INSERT触发器带双引号，创建成功
CREATE TRIGGER "Header" BEFORE INSERT ON test_trigger_src_tbl FOR EACH ROW EXECUTE PROCEDURE tri_insert_func();
/
DROP TRIGGER "Header" ON test_trigger_src_tbl CASCADE;

--关键字explain作为触发器名，加单引号，合理报错
--创建INSERT触发器带单引号，合理报错
CREATE TRIGGER 'Header' BEFORE INSERT ON test_trigger_src_tbl FOR EACH ROW EXECUTE PROCEDURE tri_insert_func();
/

--关键字explain作为触发器名，带反引号，合理报错
--创建INSERT触发器带反单引号，合理报错
CREATE TRIGGER `Header` BEFORE INSERT ON test_trigger_src_tbl FOR EACH ROW EXECUTE PROCEDURE tri_insert_func();
/

--清理环境
DROP FUNCTION tri_insert_func;
DROP TABLE IF EXISTS test_trigger_src_tbl;
DROP TABLE IF EXISTS test_trigger_des_tbl;