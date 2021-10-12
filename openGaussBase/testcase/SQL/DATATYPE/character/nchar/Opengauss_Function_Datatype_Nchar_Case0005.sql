-- @testpoint: 插入正常范围值，字节长度设定为8000

DECLARE
  V_C nchar(8000);
BEGIN
  DROP TABLE IF EXISTS test_nchar_05;
  CREATE TABLE test_nchar_05 (stringv nchar(8000));
  FOR I IN 1 .. 8000 LOOP
    V_C := V_C || 'x';
  END LOOP;
  insert into test_nchar_05 values (V_C);
END;
/
select * from test_nchar_05;
drop table test_nchar_05;