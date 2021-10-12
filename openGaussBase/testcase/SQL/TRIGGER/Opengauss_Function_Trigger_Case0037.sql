-- @testpoint: 创建INSTEAD OF触发器，不与WHEN条件同时使用
-- @modified at: 2020-12-18

--创建源视图和触发表
DROP TABLE IF EXISTS test_trigger_src_tbl;
DROP VIEW IF EXISTS test_trigger_src_view;
CREATE TABLE test_trigger_src_tbl(id1 INT, id2 INT, id3 INT);
CREATE VIEW test_trigger_src_view AS SELECT * FROM test_trigger_src_tbl WHERE id1<10;

--创建触发器函数
CREATE OR REPLACE FUNCTION tri_insert_func01() RETURNS TRIGGER AS
$$
DECLARE
BEGIN
    INSERT INTO test_trigger_src_tbl VALUES(NEW.id1, NEW.id2, NEW.id3);
	RETURN NEW;
END
$$ LANGUAGE PLPGSQL;
/

--创建触发器
CREATE TRIGGER insert_trigger01 INSTEAD OF INSERT ON test_trigger_src_view FOR EACH ROW EXECUTE PROCEDURE tri_insert_func01();
/

--执行INSERT触发事件
INSERT INTO test_trigger_src_view VALUES(1,2,3);
INSERT INTO test_trigger_src_view VALUES(5,6,7);
INSERT INTO test_trigger_src_view VALUES(11,22,33);
INSERT INTO test_trigger_src_view VALUES(55,66,77);

--检查触发结果
SELECT * FROM test_trigger_src_tbl;
SELECT * FROM test_trigger_src_view;

--DROP TRIGGER
DROP TRIGGER insert_trigger01 ON test_trigger_src_view;
DROP FUNCTION tri_insert_func01() cascade;
DROP VIEW test_trigger_src_view;
DROP TABLE test_trigger_src_tbl;