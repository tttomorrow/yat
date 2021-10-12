-- @testpoint: 对全局临时表创建触发器，不支持，合理报错
-- @modified at: 2020-12-15

----创建源表和触发表
DROP TABLE IF EXISTS test_trigger_src_tbl0;
DROP TABLE IF EXISTS test_trigger_des_tbl0;
CREATE GLOBAL TEMPORARY TABLE  test_trigger_src_tbl0(id1 INT, id2 INT, id3 INT);
CREATE GLOBAL TEMPORARY TABLE  test_trigger_des_tbl0(id1 INT, id2 INT, id3 INT);

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

----清理资源
DROP FUNCTION tri_insert_func01();
DROP TABLE test_trigger_src_tbl0;
DROP TABLE test_trigger_des_tbl0;