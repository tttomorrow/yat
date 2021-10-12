-- @testpoint: 删除触发器函数获取delete触发器的定义信息以pretty方式展示
-- @modified at: 2020-12-21

--创建源表和触发表
DROP TABLE IF EXISTS test_trigger_src_tbl;
DROP TABLE IF EXISTS test_trigger_des_tbl;
CREATE TABLE test_trigger_src_tbl(id1 INT, id2 INT, id3 INT);
CREATE TABLE test_trigger_des_tbl(id1 INT, id2 INT, id3 INT);

--创建触发器函数
CREATE OR REPLACE FUNCTION TRI_DELETE_FUNC() RETURNS TRIGGER AS
$$
DECLARE
BEGIN
	DELETE FROM test_trigger_des_tbl WHERE id1=OLD.id1;
	RETURN OLD;
END
$$ LANGUAGE PLPGSQL;
/

--创建触发器
CREATE TRIGGER delete_trigger BEFORE DELETE ON test_trigger_src_tbl FOR EACH ROW EXECUTE PROCEDURE tri_delete_func();
/

--删除触发器函数获取delete触发器的定义信息以pretty方式展示
DROP TRIGGER delete_trigger ON test_trigger_src_tbl;
SELECT pg_get_triggerdef(oid,true) FROM pg_trigger WHERE oid IN (SELECT oid FROM pg_trigger where tgname='delete_trigger');

--清理资源
DROP FUNCTION TRI_DELETE_FUNC() cascade;
DROP TABLE test_trigger_src_tbl;
DROP TABLE test_trigger_des_tbl;