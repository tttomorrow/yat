-- @testpoint: 指定触发器的触发频率为FOR EACH STATEMENT

--创建源表及触发表
DROP TABLE IF EXISTS test_trigger_src_tbl;
DROP TABLE IF EXISTS test_trigger_des_tbl;
CREATE TABLE test_trigger_src_tbl(id1 INT, id2 INT, id3 INT);
CREATE TABLE test_trigger_des_tbl(id1 INT, id2 INT, id3 INT);

--创建触发器函数
CREATE OR REPLACE FUNCTION tri_insert_func01() RETURNS TRIGGER AS
$$
DECLARE
BEGIN
    INSERT INTO test_trigger_des_tbl VALUES(7,8,9);
    RETURN NEW;
END
$$ LANGUAGE PLPGSQL;
/

--创建INSERT触发器
CREATE TRIGGER insert_trigger01 AFTER INSERT ON test_trigger_src_tbl FOR EACH STATEMENT EXECUTE PROCEDURE tri_insert_func01();
/

--执行INSERT触发事件并检查触发结果
INSERT INTO test_trigger_src_tbl VALUES(100,200,300);
INSERT INTO test_trigger_src_tbl VALUES(400,500,600);
SELECT * FROM test_trigger_src_tbl;
SELECT * FROM test_trigger_des_tbl;

--清理环境
DROP TRIGGER insert_trigger01 ON test_trigger_src_tbl;
DROP FUNCTION tri_insert_func01() cascade;
DROP TABLE test_trigger_src_tbl;
DROP TABLE test_trigger_des_tbl;