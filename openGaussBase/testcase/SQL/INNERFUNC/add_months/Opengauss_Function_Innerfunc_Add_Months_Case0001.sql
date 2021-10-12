-- @testpoint: 1.测试add_months的输入参数格式类型

select ADD_MONTHS('20180228',null) FROM sys_dummy;
select ADD_MONTHS('2018-02-28',1) FROM sys_dummy;
select ADD_MONTHS('2018-02-28',-1) FROM sys_dummy;
select ADD_MONTHS('2018-02-28',-1) FROM sys_dummy;