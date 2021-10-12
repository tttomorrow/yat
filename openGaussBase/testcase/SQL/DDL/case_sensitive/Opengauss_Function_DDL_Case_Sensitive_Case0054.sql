--  @testpoint: 创建触发器验证名称大小写

--创建源表及触发表
DROP TABLE IF EXISTS test_trigger_src_tbl CASCADE;
DROP TABLE IF EXISTS test_trigger_des_tbl CASCADE;
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
--创建INSERT触发器
CREATE TRIGGER insert_trigger BEFORE INSERT ON test_trigger_src_tbl FOR EACH ROW EXECUTE PROCEDURE tri_insert_func();
/
CREATE TRIGGER INSERT_TRIGGER BEFORE INSERT ON test_trigger_src_tbl FOR EACH ROW EXECUTE PROCEDURE tri_insert_func();
/
DROP TABLE IF EXISTS test_trigger_src_tbl CASCADE;
DROP TABLE IF EXISTS test_trigger_des_tbl CASCADE;