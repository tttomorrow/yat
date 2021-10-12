-- @testpoint: DROP TRIGGER不带table_name，合理报错

--创建表
CREATE TABLE test_trigger_src_tbl0(id1 INT, id2 INT, id3 INT) WITH (ORIENTATION = ROW);
CREATE TABLE test_trigger_des_tbl0(id1 INT, id2 INT, id3 INT);


--创建触发器函数
CREATE OR REPLACE FUNCTION tri_insert_func01() RETURNS TRIGGER AS
$$
DECLARE
BEGIN
	INSERT INTO test_trigger_des_tbl0 VALUES(NEW.id1, NEW.id2, NEW.id3);
	RETURN NEW;
END
$$ LANGUAGE PLPGSQL;
/

--创建触发器
CREATE TRIGGER insert_trigger01 BEFORE INSERT ON test_trigger_src_tbl0 FOR EACH ROW EXECUTE PROCEDURE tri_insert_func01();
/

--DROP TRIGGER
DROP TRIGGER insert_trigger01;
DROP FUNCTION tri_insert_func01() cascade;
DROP TABLE test_trigger_src_tbl0;
DROP TABLE test_trigger_des_tbl0;