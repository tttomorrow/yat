-- @testpoint: TRUNCATE类型触发器不支持FOR EACH ROW触发频率，合理报错

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

--创建触发器,指定为for each row
CREATE TRIGGER truncate_trigger BEFORE TRUNCATE ON test_trigger_src_tbl FOR EACH ROW EXECUTE PROCEDURE TRI_TRUNCATE_FUNC();
/

--清理资源
DROP FUNCTION TRI_TRUNCATE_FUNC() cascade;
DROP TABLE test_trigger_src_tbl;
DROP TABLE test_trigger_des_tbl;