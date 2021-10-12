-- @testpoint: 字符处理函数length与case when联合使用
select case when 2>1 then length(ADD_MONTHS(to_date('2016-02-29','yyyy-mm-dd'),1)) else '0' end from sys_dummy;
