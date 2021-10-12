-- @testpoint: 3.测试add_months的应用场景:测试add_months的运算
select (ADD_MONTHS('2018-02-28',2)-ADD_MONTHS('2018-02-28',-2)) from sys_dummy;
select (ADD_MONTHS('2018-02-28',2)-ADD_MONTHS('2018-02-28',-1))/10 from sys_dummy;