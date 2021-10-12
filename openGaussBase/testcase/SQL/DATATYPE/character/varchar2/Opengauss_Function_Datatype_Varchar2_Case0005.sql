-- @testpoint: 插入正常范围值，字节长度设定为合理范围值（800）
-- @modify at: 2020-11-17

DECLARE
  V_C varchar2(800);
BEGIN
  drop table if exists test_varchar2_05;
  create table test_varchar2_05 (name varchar2(800));
  FOR I IN 1 .. 800 LOOP
    V_C := V_C || 'q';
  END LOOP;
  insert into test_varchar2_05 values (V_C);
END;
/
select * from test_varchar2_05;
drop table test_varchar2_05;