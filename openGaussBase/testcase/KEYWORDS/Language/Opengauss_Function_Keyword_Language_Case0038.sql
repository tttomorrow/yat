--  @testpoint:opengauss关键字Language(非保留),LANGUAGE plpgsql创建触发器

drop table if exists test_trigger_src_tbl;
CREATE TABLE test_trigger_src_tbl(id1 INT, id2 INT, id3 INT);
drop table if exists test_trigger_des_tbl;
CREATE TABLE test_trigger_des_tbl(id1 INT, id2 INT, id3 INT);


CREATE OR REPLACE FUNCTION tri_insert_func() RETURNS TRIGGER AS
           $$
           DECLARE
           BEGIN
                   INSERT INTO test_trigger_des_tbl VALUES(NEW.id1, NEW.id2, NEW.id3);
                   RETURN NEW;
           END
           $$ LANGUAGE PLPGSQL;
/
select * from tri_insert_func;

drop FUNCTION tri_insert_func;

drop table test_trigger_src_tbl;

drop table test_trigger_des_tbl;
