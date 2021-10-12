-- @testpoint: 删除触发器函数获取truncate触发器的定义信息
-- @modified at: 2020-12-21

--创建源表和触发表
DROP TABLE IF EXISTS test_trigger_src_tbl;
DROP TABLE IF EXISTS test_trigger_des_tbl;
CREATE TABLE test_trigger_src_tbl(id1 INT, id2 INT, id3 INT);
CREATE TABLE test_trigger_des_tbl(id1 INT, id2 INT, id3 INT);

--创建触发器函数
CREATE OR REPLACE FUNCTION TRI_TRUNCATE_FUNC() RETURNS TRIGGER AS
$$
DECLARE
BEGIN
	TRUNCATE test_trigger_des_tbl;
	RETURN OLD;
END
$$ LANGUAGE PLPGSQL;
/

--创建触发器
CREATE TRIGGER truncate_trigger BEFORE TRUNCATE ON test_trigger_src_tbl EXECUTE PROCEDURE TRI_TRUNCATE_FUNC();
/

--删除触发器函数获取truncate触发器的定义信息
DROP TRIGGER truncate_trigger ON test_trigger_src_tbl;
SELECT pg_get_triggerdef(oid) FROM pg_trigger WHERE oid IN (SELECT oid FROM pg_trigger where tgname='truncate_trigger');

--清理资源
DROP FUNCTION TRI_TRUNCATE_FUNC() cascade;
DROP TABLE test_trigger_src_tbl;
DROP TABLE test_trigger_des_tbl;