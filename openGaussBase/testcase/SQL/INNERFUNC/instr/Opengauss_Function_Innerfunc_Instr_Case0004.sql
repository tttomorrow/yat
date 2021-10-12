-- @testpoint: instr函数测试，参数个数缺少或参数个数超出规定，合理报错
SELECT instr('wo') AS RESULT from sys_dummy;
SELECT instr(,'wo',1,1) AS RESULT from sys_dummy;
SELECT instr() AS RESULT from sys_dummy;
SELECT instr('womende','wo','d',1,1) AS RESULT from sys_dummy;
SELECT instr(12:12,12,1,1) AS RESULT from sys_dummy;
