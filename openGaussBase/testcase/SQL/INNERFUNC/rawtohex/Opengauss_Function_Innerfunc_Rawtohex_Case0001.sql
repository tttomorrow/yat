-- @testpoint: rawtohex函数与其它函数嵌套使用
select TO_CHAR(rawtohex(SUBSTR('CERTPIC',4,1)));