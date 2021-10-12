-- @testpoint: unknow类型测试

--testpoint：unknow+unknow类型 可隐式转换：success
explain performance select 123456 || 789;
explain performance select 123456 >= 789;
explain performance select 123456 % 789;
explain performance SELECT  '192.168.1/24' <<=  '192.168.1/24';
explain performance select   'test' !~~  'test';

--testpoint：unknow+已知类型 可隐式转换：success
explain performance select 123456::text || 789 || 123::text;
explain performance select 123456 >= '789'::clob;
explain performance select 123456 % '789'::clob;
explain performance SELECT inet '192.168.1/24' <<=  '192.168.1/24';
explain performance select   'test'::clob !~~  'test';

--环境清理
--no need to clean