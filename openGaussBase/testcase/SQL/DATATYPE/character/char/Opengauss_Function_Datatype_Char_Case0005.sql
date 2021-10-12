-- @testpoint: 插入正常值，超出字节长度设定，合理报错
-- @modify at: 2020-11-05

DECLARE
  V_C char(801);
BEGIN
  DROP TABLE IF EXISTS test_char_05;
  CREATE TABLE test_char_05 (stringv char(800));
  FOR I IN 1 .. 801 LOOP
    V_C := V_C || 'x';
  END LOOP;
  insert into test_char_05 values (V_C);
END;
/

drop table test_char_05;
