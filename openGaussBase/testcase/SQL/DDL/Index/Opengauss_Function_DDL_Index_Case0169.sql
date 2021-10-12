-- @testpoint: 触发器：alter索引不可用，插入数据后再reindex

--建普通表
DROP TABLE if EXISTS test_index_table_169 CASCADE;
create table test_index_table_169(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

drop index if exists index_169_01;
create index index_169_01 on test_index_table_169(c_int) local (PARTITION p1,PARTITION p2,PARTITION p3,PARTITION p4);

--创建触发器函数
CREATE OR REPLACE FUNCTION index_fun_169_01() RETURNS TRIGGER AS
           $$
           DECLARE
           BEGIN
                   REINDEX index index_169_01;
                   RETURN NEW;
           END
           $$ LANGUAGE PLPGSQL;
/


drop TRIGGER if exists index_trigger_169_01 on test_index_table_169 cascade;
CREATE TRIGGER index_trigger_169_01
           after insert  ON test_index_table_169
           FOR EACH ROW
           EXECUTE PROCEDURE index_fun_169_01();
/

--调用触发器
explain select * from test_index_table_169 where c_int > 500 group by c_int;
alter index index_169_01 UNUSABLE;
explain select * from test_index_table_169 where c_int > 500 group by c_int;
insert into test_index_table_169 values(0),(1),(2);
explain select * from test_index_table_169 where c_int > 500 group by c_int;

--清理环境
drop table test_index_table_169 cascade;
drop function if exists index_fun_169_01;