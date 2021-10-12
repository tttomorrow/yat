-- @testpoint: openGauss保留关键字default作为触发器名，不带引号，部分测试点合理报错
--前提条件
--创建源表
drop table if exists test_trigger_src_tbl;
CREATE TABLE test_trigger_src_tbl(id1 INT, id2 INT, id3 INT);

--创建触发表
drop table if exists test_trigger_des_tbl;
CREATE TABLE test_trigger_des_tbl(id1 INT, id2 INT, id3 INT);

 -----创建触发器函数
 CREATE OR REPLACE FUNCTION tri_insert_func() RETURNS TRIGGER AS
           $$
           DECLARE
           BEGIN
                   INSERT INTO test_trigger_des_tbl VALUES(NEW.id1, NEW.id2, NEW.id3);
                   RETURN NEW;
           END
           $$ LANGUAGE PLPGSQL;
           /


 --创建INSERT触发器，default作为作为触发器名，不带引号，合理报错

CREATE TRIGGER default
           BEFORE INSERT ON test_trigger_src_tbl
           FOR EACH ROW
           EXECUTE PROCEDURE tri_insert_func();
/
------------------------------------------------
--openGauss保留关键字default作为触发器名，加双引号，创建成功

CREATE TRIGGER "default"
           BEFORE INSERT ON test_trigger_src_tbl
           FOR EACH ROW
           EXECUTE PROCEDURE tri_insert_func();
/
drop TRIGGER "default" on test_trigger_src_tbl cascade;
------------------------------------------------------
--openGauss保留关键字default作为触发器名，加单引号，合理报错

CREATE TRIGGER 'default'
           BEFORE INSERT ON test_trigger_src_tbl
           FOR EACH ROW
           EXECUTE PROCEDURE tri_insert_func();
/
  ----------------------------------------------------------------------
  --openGauss保留关键字default作为触发器名，带反引号，合理报错

CREATE TRIGGER `default`
           BEFORE INSERT ON test_trigger_src_tbl
           FOR EACH ROW
           EXECUTE PROCEDURE tri_insert_func();

/
drop table if exists test_trigger_src_tbl;
drop table if exists test_trigger_des_tbl;
drop function if exists tri_insert_func;