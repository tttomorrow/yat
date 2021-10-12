-- @testpoint: 参数为非boolean类型，获取update触发器的定义信息，合理报错
-- @modified at: 2020-12-21

--创建源表和触发表
DROP TABLE IF EXISTS test_trigger_src_tbl;
DROP TABLE IF EXISTS test_trigger_des_tbl;
CREATE TABLE test_trigger_src_tbl(id1 INT, id2 INT, id3 INT);
CREATE TABLE test_trigger_des_tbl(id1 INT, id2 INT, id3 INT);

--创建触发器函数
CREATE OR REPLACE FUNCTION tri_update_func() RETURNS TRIGGER AS
$$
DECLARE
BEGIN
	UPDATE test_trigger_des_tbl SET id3 = NEW.id3 WHERE id1=OLD.id1;
	RETURN OLD;
END
$$ LANGUAGE PLPGSQL;
/

--创建触发器
CREATE TRIGGER update_trigger AFTER UPDATE ON test_trigger_src_tbl FOR EACH ROW EXECUTE PROCEDURE tri_update_func();
/

--参数为非boolean类型，获取update触发器的定义信息
SELECT pg_get_triggerdef(oid,'eeer') FROM pg_trigger WHERE oid IN (SELECT oid FROM pg_trigger where tgname='update_trigger');

--清理资源
DROP TRIGGER update_trigger ON test_trigger_src_tbl;
DROP FUNCTION tri_update_func() cascade;
DROP TABLE test_trigger_src_tbl;
DROP TABLE test_trigger_des_tbl;