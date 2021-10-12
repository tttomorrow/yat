-- @testpoint: 插入数据为拼接字符串,超出字节设定长度，合理报错

DECLARE
  V_C character(8000);
BEGIN
  drop table if exists test_character_08;
  create table test_character_08 (name character(8000));
  FOR I IN 1 .. 7998 LOOP
    V_C := V_C || 'q';
  END LOOP;
  insert into test_character_08 values (V_C);
END;
/
insert into test_character_08 select name||'wxxxxxxxxxw' from test_character_08;
drop table test_character_08;