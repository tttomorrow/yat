--  @testpoint: 删除同名词，区分同名词的大小写
drop synonym if exists VI ;
drop synonym if exists vi;
DROP SYNONYM if exists AD;
SELECT * FROM pg_synonym WHERE synname='ad';
SELECT * FROM pg_synonym WHERE synname='AD';
drop synonym if exists ad;