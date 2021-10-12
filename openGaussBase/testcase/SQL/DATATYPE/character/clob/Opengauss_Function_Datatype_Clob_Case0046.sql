-- @testpoint: 插入正常值，支持多次拼接
-- @modified at: 2020-11-13

DECLARE
  V_C varchar(80);
BEGIN
  drop table if exists test_clob_046;
  create table test_clob_046 (name clob);
  FOR I IN 1 .. 80 LOOP
    V_C := V_C || 'q';
  END LOOP;
  insert into test_clob_046 values (V_C);
END;
/
insert into test_clob_046 select name||'ww'||'aaaa'||'bbbb' from test_clob_046;
select * from test_clob_046;
drop table test_clob_046;