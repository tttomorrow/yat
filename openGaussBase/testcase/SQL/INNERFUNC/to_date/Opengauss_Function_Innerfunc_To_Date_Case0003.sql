-- @testpoint: to_date函数，将文本类型的值转换为指定格式的时间戳，参数多/少输入的函数测试，合理报错

select to_date('2018','yyyy','2018','yyyy');
select to_date('2018-01-15','yyyy-mm','dd');