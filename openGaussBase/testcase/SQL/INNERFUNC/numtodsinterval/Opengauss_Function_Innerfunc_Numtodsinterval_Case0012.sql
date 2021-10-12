-- @testpoint: numtodsinterval函数interval_unit为'HOUR',兼容格式输出
SET intervalstyle = a;
SELECT numtodsinterval(100, 'HOUR') from sys_dummy;
