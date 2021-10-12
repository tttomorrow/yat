-- @testpoint: 禁用TRUNCATE触发器
--创建表
CREATE TABLE test_trigger_src_tbl0(id1 INT, id2 INT, id3 INT);
INSERT INTO test_trigger_src_tbl0 VALUES(100,200,300);
CREATE TABLE test_trigger_des_tbl0(id1 INT, id2 INT, id3 INT);
INSERT INTO test_trigger_des_tbl0 VALUES(1,2,3);

--创建触发器函数
CREATE OR REPLACE FUNCTION tri_truncate_func01() RETURNS TRIGGER AS
$$
DECLARE
BEGIN
	truncate table test_trigger_des_tbl0;
RETURN NEW;
END
$$ LANGUAGE PLPGSQL;
/

--创建触发器
CREATE TRIGGER truncate_trigger01 BEFORE truncate ON test_trigger_src_tbl0 FOR EACH STATEMENT EXECUTE PROCEDURE tri_truncate_func01();
/
--禁用触发器
ALTER TABLE test_trigger_src_tbl0 DISABLE TRIGGER truncate_trigger01;  

--执行触发事件
truncate table test_trigger_src_tbl0;
SELECT * FROM test_trigger_src_tbl0;

--检查触发结果
SELECT * FROM test_trigger_des_tbl0;

--DROP TRIGGER
DROP TRIGGER IF EXISTS truncate_trigger01 ON test_trigger_src_tbl0;
DROP FUNCTION tri_truncate_func01() cascade;
DROP TABLE test_trigger_src_tbl0;
DROP TABLE test_trigger_des_tbl0;