-- @testpoint: 插入正常值，超出字节长度设定长度，合理报错
-- @modify at: 2020-11-05


DECLARE
  V_C character(8001);
BEGIN
  drop table if exists test_character_06;
  create table test_character_06 (name character(8000));
  FOR I IN 1 .. 8001 LOOP
    V_C := V_C || 'q';
  END LOOP;
  insert into test_character_06 values (V_C);
END;
/

drop table test_character_06;