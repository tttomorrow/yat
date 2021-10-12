-- @testpoint: 为同一事件定义多个相同类型的触发器，则按触发器的名称字母顺序触发
-- @modified at: 2020-12-16

----创建源表和触发表
DROP TABLE IF EXISTS test_trigger_src_tbl0;
DROP TABLE IF EXISTS test_trigger_des_tbl0;
CREATE TABLE test_trigger_src_tbl0(id1 int, id2 int, id3 int);
CREATE TABLE test_trigger_des_tbl0(id1 INT, id2 INT, id3 INT);
    

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
CREATE TRIGGER a_insert_trigger01 BEFORE INSERT ON test_trigger_src_tbl0 FOR EACH ROW EXECUTE PROCEDURE tri_insert_func01();
/
CREATE TRIGGER b_insert_trigger01 BEFORE INSERT ON test_trigger_src_tbl0 FOR EACH ROW EXECUTE PROCEDURE tri_insert_func01();
/

----执行INSERT触发事件
INSERT INTO test_trigger_src_tbl0 VALUES(100,200,300);
INSERT INTO test_trigger_src_tbl0 VALUES(400,500,600);
INSERT INTO test_trigger_src_tbl0 VALUES(700,800,900);
SELECT * FROM test_trigger_src_tbl0;

----检查触发结果
SELECT * FROM test_trigger_des_tbl0;
----清理资源
DROP TRIGGER a_insert_trigger01 ON test_trigger_src_tbl0;
DROP TRIGGER b_insert_trigger01 ON test_trigger_src_tbl0;
DROP FUNCTION tri_insert_func01();
DROP TABLE test_trigger_src_tbl0;
DROP TABLE test_trigger_des_tbl0;
