-- @testpoint: 插入中文


DECLARE
  V_C varchar(1000);
BEGIN
  drop table if exists test_varchar_10;
  create table test_varchar_10 (name varchar(1000));
  FOR I IN 1 .. 333 LOOP
    V_C := V_C || '中';
  END LOOP;
  insert into test_varchar_10 values (V_C);
END;
/
select * from test_varchar_10;
drop table test_varchar_10;