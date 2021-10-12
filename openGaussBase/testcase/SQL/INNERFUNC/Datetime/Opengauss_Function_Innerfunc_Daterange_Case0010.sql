-- @testpoint: daterange函数给定 text为错误参数，合理报错

select daterange('2000-05-06','2000-08-08','abc');
