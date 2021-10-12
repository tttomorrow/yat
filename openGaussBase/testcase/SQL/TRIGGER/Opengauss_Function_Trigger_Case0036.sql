-- @testpoint: INSTEAD OF触发器不支持WHEN条件，合理报错
--创建视图
CREATE VIEW test_trigger_src_tbl0 AS SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
CREATE VIEW test_trigger_des_tbl0 AS SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
CREATE TABLE test_trigger_src_tb2(id1 INT, id2 INT, id3 INT);

--创建触发器函数
CREATE OR REPLACE FUNCTION tri_insert_func01() RETURNS TRIGGER AS
$$
DECLARE
BEGIN
	DROP VIEW test_trigger_des_tbl0 CASCADE;
END
$$ LANGUAGE PLPGSQL;
/
--创建触发器
CREATE TRIGGER insert_trigger01 instead of INSERT ON test_trigger_src_tbl0 FOR EACH ROW WHEN(NEW.id1) EXECUTE PROCEDURE tri_insert_func01();
/
--执行INSERT触发事件
INSERT INTO test_trigger_src_tb2 VALUES(100,200,300);
SELECT * FROM test_trigger_src_tb2;
--检查触发结果
SELECT * FROM test_trigger_des_tbl0;
--DROP TRIGGER
DROP TRIGGER IF EXISTS insert_trigger01 ON test_trigger_src_tbl0;
DROP FUNCTION tri_insert_func01() cascade;
DROP VIEW test_trigger_src_tbl0;
DROP VIEW test_trigger_des_tbl0;
DROP TABLE test_trigger_src_tb2;