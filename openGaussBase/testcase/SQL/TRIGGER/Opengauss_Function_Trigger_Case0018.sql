-- @testpoint: 创建触发器,触发器名长度为62个字符
-- @modified at: 2020-12-16

----创建表
CREATE TABLE test_trigger_src_tbl0(id1 int,id2 int, id3 int) PARTITION BY RANGE (id1) (PARTITION P1 VALUES LESS THAN(5000));

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
CREATE TRIGGER insert_trigger01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab BEFORE INSERT ON test_trigger_src_tbl0 FOR EACH ROW EXECUTE PROCEDURE tri_insert_func01();
/

----查看触发器名称
select tgname from pg_trigger;

----清理资源
DROP TRIGGER insert_trigger01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab ON test_trigger_src_tbl0;
DROP FUNCTION tri_insert_func01();
DROP TABLE test_trigger_src_tbl0;
