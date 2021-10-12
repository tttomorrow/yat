-- @testpoint: 对分区表创建触发器
-- @modified at: 2020-12-15

----创建源表和触发表
DROP TABLE IF EXISTS test_trigger_src_tbl0;
DROP TABLE IF EXISTS test_trigger_des_tbl0;
CREATE TABLE test_trigger_src_tbl0(id1 int,id2 int, id3 int) PARTITION BY RANGE (id1) (PARTITION P1 VALUES LESS THAN(5000));
CREATE TABLE test_trigger_des_tbl0(id1 int,id2 int, id3 int) PARTITION BY RANGE (id1) (PARTITION P1 VALUES LESS THAN(5000));

----创建触发器函数
CREATE OR REPLACE FUNCTION tri_insert_func01() RETURNS TRIGGER AS
$$
DECLARE
BEGIN
	INSERT INTO test_trigger_des_tbl0 VALUES(NEW.id1, NEW.id2, NEW.id3);
	RETURN NEW;
END
$$ LANGUAGE PLPGSQL;
/

----创建触发器
CREATE TRIGGER insert_trigger01 BEFORE INSERT ON test_trigger_src_tbl0 FOR EACH ROW EXECUTE PROCEDURE tri_insert_func01();
/

----执行INSERT触发事件
INSERT INTO test_trigger_src_tbl0 VALUES(100,200,300);
INSERT INTO test_trigger_src_tbl0 VALUES(100,200,300);
INSERT INTO test_trigger_src_tbl0 VALUES(100,200,300);
SELECT * FROM test_trigger_src_tbl0;

----检查触发结果
SELECT * FROM test_trigger_des_tbl0;
----清理资源
DROP TRIGGER insert_trigger01 ON test_trigger_src_tbl0;
DROP FUNCTION tri_insert_func01();
DROP TABLE test_trigger_src_tbl0;
DROP TABLE test_trigger_des_tbl0;