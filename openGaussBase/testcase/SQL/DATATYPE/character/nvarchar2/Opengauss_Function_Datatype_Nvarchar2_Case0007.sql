-- @testpoint: 插入数据为拼接字符串超出设定长度,合理报错

DECLARE
  V_C nvarchar2(8000);
BEGIN
  drop table if exists test_nvarchar2_07;
  create table test_nvarchar2_07 (name nvarchar2(8000));
  FOR I IN 1 .. 7998 LOOP
    V_C := V_C || 'q';
  END LOOP;
  insert into test_nvarchar2_07 values (V_C);
END;
/
insert into test_nvarchar2_07 select name||'wwdwedfsafwqweq' from test_nvarchar2_07;
drop table test_nvarchar2_07;