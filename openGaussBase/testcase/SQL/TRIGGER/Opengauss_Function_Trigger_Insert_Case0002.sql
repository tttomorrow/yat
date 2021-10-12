-- @testpoint: 删除关联表后获取insert触发器的定义信息
-- @modified at: 2020-12-21

--创建源表和触发表
DROP TABLE IF EXISTS test_trigger_src_tbl;
DROP TABLE IF EXISTS test_trigger_des_tbl;
CREATE TABLE test_trigger_src_tbl(id1 INT, id2 INT, id3 INT);
CREATE TABLE test_trigger_des_tbl(id1 INT, id2 INT, id3 INT);
--创建触发器函数
CREATE OR REPLACE FUNCTION tri_insert_func() RETURNS TRIGGER AS
$$
DECLARE
BEGIN
	INSERT INTO test_trigger_des_tbl VALUES(NEW.id1, NEW.id2, NEW.id3);
	RETURN NEW;
END
$$ LANGUAGE PLPGSQL;
/

--创建触发器
CREATE TRIGGER insert_trigger BEFORE INSERT ON test_trigger_src_tbl FOR EACH ROW EXECUTE PROCEDURE tri_insert_func();
/

--删除关联触发表，获取insert触发器的定义信息
DROP TABLE test_trigger_des_tbl;
SELECT pg_get_triggerdef(oid) FROM pg_trigger WHERE oid IN (SELECT oid FROM pg_trigger where tgname='insert_trigger');

--清理资源
DROP TRIGGER insert_trigger ON test_trigger_src_tbl;
DROP FUNCTION tri_insert_func() cascade;
DROP TABLE test_trigger_src_tbl;