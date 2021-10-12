-- @testpoint: 字符处理函数length与时间函数嵌套测试
select length(ADD_MONTHS(to_date('2017-01-29','yyyy-mm-dd'),1)) from sys_dummy;
select length(EXTRACT (MONTH FROM DATE '2018-10-04')) from sys_dummy;
