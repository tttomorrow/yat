-- @testpoint: opengauss逻辑操作符OR,与NOT运算优先级
select 1 or not 1;
select 1 or not 0;
select 0 or not 1;
select 0 or not 0;