-- @testpoint: 不支持TRIGGER中调用含有COMMIT/ROLLBACK的存储过程，合理报错

--创建源表及触发表
DROP TABLE IF EXISTS test_trigger_src_tbl;
DROP TABLE IF EXISTS test_trigger_des_tbl;
CREATE TABLE test_trigger_src_tbl(id1 INT, id2 INT, id3 INT);
CREATE TABLE test_trigger_des_tbl(id1 INT, id2 INT, id3 INT);

--创建触发器函数
CREATE OR REPLACE FUNCTION tri_insert_func01() RETURN TRIGGER
AS
EXP INT;
BEGIN
    FOR i IN 0..20 LOOP
        INSERT INTO test_trigger_des_tbl(id1) VALUES (i);
        IF i % 2 = 0 THEN
            COMMIT;
        ELSE
            ROLLBACK;
        END IF;
    END LOOP;
    SELECT COUNT(*) FROM test_trigger_des_tbl INTO EXP;
END;
/

--创建INSERT触发器
CREATE TRIGGER insert_trigger01 BEFORE INSERT ON test_trigger_src_tbl FOR EACH ROW EXECUTE PROCEDURE tri_insert_func01();
/

--执行INSERT触发事件并检查触发结果
INSERT INTO test_trigger_src_tbl VALUES(100,200,300);
SELECT * FROM test_trigger_src_tbl;
SELECT * FROM test_trigger_des_tbl;

--清理环境
DROP TRIGGER insert_trigger01 ON test_trigger_src_tbl;
DROP FUNCTION tri_insert_func01() cascade;
DROP TABLE test_trigger_src_tbl;
DROP TABLE test_trigger_des_tbl;