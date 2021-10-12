-- @testpoint: 插入数据为拼接字符串超出设定长度测试,合理报错


DECLARE
  V_C varchar(8000);
BEGIN
  drop table if exists test_varchar_09;
  create table test_varchar_09 (name varchar(8000));
  FOR I IN 1 .. 8000 LOOP
    V_C := V_C || 'q';
  END LOOP;
  insert into test_varchar_09 values (V_C);
END;
/
insert into test_varchar_09 select substr(name,1,7999)||'xxxxxxxxx' from test_varchar_09;

drop table test_varchar_09;