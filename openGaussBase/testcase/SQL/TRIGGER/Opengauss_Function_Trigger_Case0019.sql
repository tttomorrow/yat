-- @testpoint: 统一触发器函数中指定多个触发事件
-- @modified at: 2020-12-16

----创建源表和触发表
DROP TABLE IF EXISTS test_trigger_src_tbl0;
DROP TABLE IF EXISTS test_trigger_des_tbl0;
CREATE TABLE test_trigger_src_tbl0(id1 INT, id2 INT, id3 INT);
CREATE TABLE test_trigger_des_tbl0(id1 INT, id2 INT, id3 INT);
INSERT INTO test_trigger_src_tbl0 VALUES(100,200,300);
INSERT INTO test_trigger_src_tbl0 VALUES(400,500,600);
INSERT INTO test_trigger_src_tbl0 VALUES(700,800,900);
INSERT INTO test_trigger_des_tbl0 VALUES(100,2,3);
INSERT INTO test_trigger_des_tbl0 VALUES(400,5,6);
INSERT INTO test_trigger_des_tbl0 VALUES(700,8,9);

----创建触发器函数
CREATE OR REPLACE FUNCTION tri_insert_func01() RETURNS TRIGGER AS
$$
DECLARE
BEGIN
	UPDATE test_trigger_des_tbl0 SET id3=NEW.id3 WHERE id1 = OLD.id1;
	DELETE FROM test_trigger_des_tbl0 WHERE id1 = OLD.id1;
	RETURN OLD;
END
$$ LANGUAGE PLPGSQL;
/

----创建触发器
CREATE TRIGGER insert_trigger01 BEFORE UPDATE OR DELETE ON test_trigger_src_tbl0 FOR EACH ROW EXECUTE PROCEDURE tri_insert_func01();
/

----执行INSERT触发事件并检查触发结果
UPDATE test_trigger_src_tbl0 SET id1=1 WHERE id3<800;
SELECT * FROM test_trigger_src_tbl0;
SELECT * FROM test_trigger_des_tbl0;

----执行DELETE触发事件并检查触发结果
DELETE FROM test_trigger_src_tbl0 WHERE id3 < 800;
SELECT * FROM test_trigger_src_tbl0;
SELECT * FROM test_trigger_des_tbl0;


----清理资源
DROP TRIGGER insert_trigger01 ON test_trigger_src_tbl0;
DROP FUNCTION tri_insert_func01();
DROP TABLE test_trigger_src_tbl0;
DROP TABLE test_trigger_des_tbl0;