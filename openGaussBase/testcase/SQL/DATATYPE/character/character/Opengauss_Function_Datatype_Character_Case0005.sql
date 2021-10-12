-- @testpoint: 插入正常值，字节长度设定为合理范围
-- @modify at: 2020-11-05

DECLARE
  V_C character(8000);
BEGIN
  drop table if exists test_character_05;
  create table test_character_05 (name character(8000));
  FOR I IN 1 .. 8000 LOOP
    V_C := V_C || 'q';
  END LOOP;
  insert into test_character_05 values (V_C);
END;
/
select char_length(name) from test_character_05;
drop table test_character_05;