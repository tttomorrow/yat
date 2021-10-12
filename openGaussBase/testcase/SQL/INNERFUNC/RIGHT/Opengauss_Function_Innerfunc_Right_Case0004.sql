-- @testpoint: right函数入参是null或者''
SELECT right('甘肃中滩',null)AS RESULT; 
SELECT right('甘肃中滩','')AS RESULT; 
SELECT right(null,1)AS RESULT; 
SELECT right('',1)AS RESULT; 