-- @testpoint: 插入数据为拼接字符串超出设定长度测试，合理报错

DECLARE
  V_C nchar(8000);
BEGIN
  drop table if exists test_nchar_08;
  create table test_nchar_08 (name nchar(8000));
  FOR I IN 1 .. 7998 LOOP
    V_C := V_C || 'q';
  END LOOP;
  insert into test_nchar_08 values (V_C);
END;
/
insert into test_nchar_08 select name||'wwdwedfsafwqweq' from test_nchar_08;
drop table test_nchar_08;
