-- @testpoint: BEFORE-UPDATE在表上支持语句级触发器
--创建表
CREATE TABLE test_trigger_src_tbl0(id1 INT, id2 INT, id3 INT);
INSERT INTO test_trigger_src_tbl0 VALUES(100,200,300);
CREATE TABLE test_trigger_des_tbl0(id1 INT, id2 INT, id3 INT);
INSERT INTO test_trigger_des_tbl0 VALUES(1,2,3);

--创建触发器函数
CREATE OR REPLACE FUNCTION tri_update_func01() RETURNS TRIGGER AS
$$
DECLARE
BEGIN
	UPDATE test_trigger_des_tbl0 SET id3 = 5 WHERE id1=1;
	RETURN NEW;
END
$$ LANGUAGE PLPGSQL;
/

--创建触发器
CREATE TRIGGER update_trigger01 BEFORE UPDATE ON test_trigger_src_tbl0 FOR EACH STATEMENT EXECUTE PROCEDURE tri_update_func01();
/

--执行INSERT触发事件
UPDATE test_trigger_src_tbl0 SET id3=400 WHERE id1=100;
SELECT * FROM test_trigger_src_tbl0;

--检查触发结果
SELECT * FROM test_trigger_des_tbl0;

--DROP TRIGGER
DROP TRIGGER IF EXISTS update_trigger01 ON test_trigger_src_tbl0;
DROP FUNCTION tri_update_func01() cascade;
DROP TABLE test_trigger_src_tbl0;
DROP TABLE test_trigger_des_tbl0;