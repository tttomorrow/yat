-- @testpoint: BEFORE--DELETE在表上支持行级触发器
--创建表
CREATE TABLE test_trigger_src_tbl0(id1 INT, id2 INT, id3 INT);
INSERT INTO test_trigger_src_tbl0 VALUES(100,200,300);
CREATE TABLE test_trigger_des_tbl0(id1 INT, id2 INT, id3 INT);
INSERT INTO test_trigger_des_tbl0 VALUES(1,2,3);

--创建触发器函数
CREATE OR REPLACE FUNCTION tri_delete_func0101() RETURNS TRIGGER AS
$$
DECLARE
BEGIN
	DELETE FROM test_trigger_des_tbl0 WHERE id1=1;
	RETURN OLD;
END
$$ LANGUAGE PLPGSQL;
/

--创建触发器
CREATE TRIGGER delete_trigger01 BEFORE DELETE ON test_trigger_src_tbl0 FOR EACH ROW EXECUTE PROCEDURE tri_delete_func0101();
/
--执行触发事件
DELETE FROM test_trigger_src_tbl0 WHERE id1=100;
SELECT * FROM test_trigger_src_tbl0;

--检查触发结果
SELECT * FROM test_trigger_des_tbl0;

--DROP TRIGGER
DROP TRIGGER IF EXISTS delete_trigger01 ON test_trigger_src_tbl0;
DROP FUNCTION tri_delete_func0101() cascade;
DROP TABLE test_trigger_src_tbl0;
DROP TABLE test_trigger_des_tbl0;