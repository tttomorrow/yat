-- @testpoint: to_date函数入参为表达式，合理报错
select to_date('2018-01-15',3>2);
select to_date('2018>2017','yyyy');