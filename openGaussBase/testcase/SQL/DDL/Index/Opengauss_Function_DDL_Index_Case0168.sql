-- @testpoint: 触发器：更新数据触发先drop index

--建普通表
DROP TABLE if EXISTS test_index_table_168 CASCADE;
create table test_index_table_168(
c_int int
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);
insert into test_index_table_168 values(0),(1),(2);
drop index if exists index_168_01;
create index index_168_01 on test_index_table_168(c_int) local (PARTITION p1,PARTITION p2,PARTITION p3,PARTITION p4);

--创建触发器函数
CREATE OR REPLACE FUNCTION index_fun_168_01() RETURNS TRIGGER AS
           $$
           DECLARE
           BEGIN
                   drop index index_168_01;
                   RETURN NEW;
           END
           $$ LANGUAGE PLPGSQL;
/


drop TRIGGER if exists index_trigger_168_01 on test_index_table_168 cascade;
CREATE TRIGGER index_trigger_168_01
           BEFORE UPDATE  ON test_index_table_168
           FOR EACH ROW
           EXECUTE PROCEDURE index_fun_168_01();
/

--调用触发器
select relname from pg_class where relname like 'index_168%' order by relname;
alter index index_168_01 UNUSABLE;
UPDATE  test_index_table_168 set c_int=500 where c_int=0;
select relname from pg_class where relname like 'index_168%' order by relname;

--清理环境
drop table test_index_table_168 cascade;
drop function if exists index_fun_168_01;