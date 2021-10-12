-- @testpoint: 插入正常范围值，结合截取函数及拼接字符串


DECLARE
  V_C varchar(8000);
BEGIN
  drop table if exists test_varchar_09;
  create table test_varchar_09 (name varchar(800));
  FOR I IN 1 .. 800 LOOP
    V_C := V_C || 'q';
  END LOOP;
  insert into test_varchar_09 values (V_C);
END;
/
insert into test_varchar_09 select substr(name,1,79)||'xghjkgfcg' from test_varchar_09;
select * from test_varchar_09;
drop table if exists test_varchar_09;