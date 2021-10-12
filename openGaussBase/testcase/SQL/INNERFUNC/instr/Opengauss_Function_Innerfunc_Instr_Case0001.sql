-- @testpoint: instr函数，结合插入语句使用
--建表
drop table if exists INSTR_TABLE3;
CREATE TABLE  INSTR_TABLE3( COL_INSTR1  INTEGER,COL_INSTR2  INTEGER,COL_INSTR3  INTEGER);
--插入数据
INSERT INTO INSTR_TABLE3(COL_INSTR1,COL_INSTR2,COL_INSTR3) VALUES(instr('Gaussbd','s',1,2),instr('#@$*@@**@*@#$%ssbd','@*',1,2),instr(1232.3234578,23,1,2));
SELECT * FROM INSTR_TABLE3;
--清理环境
drop table INSTR_TABLE3;
