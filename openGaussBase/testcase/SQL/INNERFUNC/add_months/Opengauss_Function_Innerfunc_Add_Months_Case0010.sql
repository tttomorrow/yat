-- @testpoint: 10. 测试add_months的参数为特殊字符，合理报错
select ADD_MONTHS(current_timestamp,'@') - current_timestamp  from  sys_dummy;
select ADD_MONTHS(current_timestamp,'*') - current_timestamp  from  sys_dummy;
select ADD_MONTHS(current_timestamp,'!') - current_timestamp  from  sys_dummy;
select ADD_MONTHS(current_timestamp,'#') - current_timestamp  from  sys_dummy;