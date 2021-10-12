-- @testpoint: 当指定WHEN时条件返回true时调用触发器函数
--创建表
CREATE TABLE test_trigger_src_tbl0(id1 INT, id2 INT, id3 INT);
INSERT INTO test_trigger_src_tbl0 VALUES(100,200,300);
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
--创建触发器
CREATE TRIGGER insert_trigger01 BEFORE INSERT ON test_trigger_src_tbl0 FOR EACH ROW WHEN(NEW.id1) EXECUTE PROCEDURE tri_insert_func01();
/
--执行INSERT触发事件
INSERT INTO test_trigger_src_tbl0 VALUES(400,500,600);
SELECT * FROM test_trigger_src_tbl0;
--检查触发结果
SELECT * FROM test_trigger_des_tbl0;
--DROP TRIGGER
DROP TRIGGER IF EXISTS insert_trigger01 ON test_trigger_src_tbl0;
DROP FUNCTION tri_insert_func01() cascade;
DROP TABLE test_trigger_src_tbl0;
DROP TABLE test_trigger_des_tbl0;