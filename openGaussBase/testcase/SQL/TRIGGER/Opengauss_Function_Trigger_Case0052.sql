-- @testpoint: 禁用所有触发器

--创建源表及触发表
CREATE TABLE test_trigger_src_tbl0(id1 INT, id2 INT, id3 INT);
CREATE TABLE test_trigger_des_tbl0(id1 INT, id2 INT, id3 INT);

--创建触发器函数
CREATE OR REPLACE FUNCTION tri_insert_func01() RETURNS TRIGGER AS
           $$
           DECLARE
           BEGIN
                   INSERT INTO test_trigger_des_tbl0 VALUES(NEW.id1, NEW.id2, NEW.id3);
                   RETURN NEW;
           END
           $$ LANGUAGE PLPGSQL;
/		  

CREATE OR REPLACE FUNCTION tri_update_func01() RETURNS TRIGGER AS
           $$
           DECLARE
           BEGIN
                   UPDATE test_trigger_des_tbl0 SET id3 = NEW.id3 WHERE id1=OLD.id1;
                   RETURN OLD;
           END
           $$ LANGUAGE PLPGSQL;

/
--创建INSERT触发器
CREATE TRIGGER insert_trigger01
           BEFORE INSERT ON test_trigger_src_tbl0
           FOR EACH ROW
           EXECUTE PROCEDURE tri_insert_func01();
/
--创建UPDATE触发器
CREATE TRIGGER update_trigger01
           AFTER UPDATE ON test_trigger_src_tbl0  
           FOR EACH ROW
           EXECUTE PROCEDURE tri_update_func01();
/		   
--禁用所有触发器
ALTER TABLE test_trigger_src_tbl0 DISABLE TRIGGER ALL;
--执行INSERT触发事件并检查触发结果
INSERT INTO test_trigger_src_tbl0 VALUES(100,200,300);
SELECT * FROM test_trigger_src_tbl0;

SELECT * FROM test_trigger_des_tbl0;

--执行UPDATE触发事件并检查触发结果
UPDATE test_trigger_src_tbl0 SET id3=400 WHERE id1=100;
SELECT * FROM test_trigger_src_tbl0;
SELECT * FROM test_trigger_des_tbl0;

--删除触发器
DROP TRIGGER insert_trigger01 ON test_trigger_src_tbl0;
DROP TRIGGER update_trigger01 ON test_trigger_src_tbl0;

--删除触发器函数
DROP FUNCTION tri_insert_func01() cascade;
DROP FUNCTION tri_update_func01() cascade;

DROP TABLE test_trigger_src_tbl0;
DROP TABLE test_trigger_des_tbl0;