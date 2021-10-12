-- @testpoint: 4.测试add_months的参数运算

select ADD_MONTHS('2018-02-28',1+2) from sys_dummy;
select ADD_MONTHS('2018-02-28',-(1-2)) from sys_dummy;
select ADD_MONTHS('2018-02-28',1*2) from sys_dummy;
select ADD_MONTHS('2018-02-28',mod(4,3)) from sys_dummy;