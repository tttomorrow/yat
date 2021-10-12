-- @testpoint: 插入数据为拼接字符串超出设定长度测试,合理报错

DECLARE
  V_C varchar2(8000);
BEGIN
  drop table if exists test_varchar2_08;
  create table test_varchar2_08 (name varchar2(8000));
  FOR I IN 1 .. 7998 LOOP
    V_C := V_C || 'q';
  END LOOP;
  insert into test_varchar2_08 values (V_C);
END;
/
insert into test_varchar2_08 select name||'wxxxxxxxxxw' from test_varchar2_08;
drop table test_varchar2_08;