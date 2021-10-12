-- @testpoint: 插入超出范围值，字节长度设定为8000，合理报错
-- @modify at: 2020-11-17

DECLARE
  V_C varchar2(8001);
BEGIN
  drop table if exists test_varchar2_06;
  create table test_varchar2_06 (name varchar2(8000));
  FOR I IN 1 .. 8001 LOOP
    V_C := V_C || 'q';
  END LOOP;
  insert into test_varchar2_06 values (V_C);
END;
/
