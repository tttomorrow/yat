-- @testpoint: to_date函数，将文本类型的值转换为指定格式的时间戳，中文参数测试，合理报错

select to_date('2018-01-15','年月日');
select to_date('时间','yyyy');