-- @testpoint: to_date函数，将文本类型的值转换为指定格式的时间戳，非法输入的函数测试，合理报错

select to_date('2018-01-15','yyyy');
select to_date('2018-01-15','yyyy-mm');
select to_date('09-18 06:25:46','yyyy-mm-dd HH:MI:SS:FF');
select to_date('2018-09 16:25:46:45354','yyyy-mm-dd hh24:mi:ss:ff');