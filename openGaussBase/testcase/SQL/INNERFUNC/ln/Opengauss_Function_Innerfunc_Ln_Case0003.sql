-- @testpoint: 自然对数lnx传入多参，合理报错
select ln(9,6) as result;
select ln(2.3,5.6) as result;
select ln('2','6') as result;