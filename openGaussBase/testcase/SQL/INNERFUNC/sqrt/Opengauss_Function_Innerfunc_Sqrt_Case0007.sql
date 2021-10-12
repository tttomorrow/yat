-- @testpoint: 输入参数为特殊类型,合理报错

SELECT  sqrt('2012.12.03') AS RESULT;
SELECT  sqrt(Ture) AS RESULT;
SELECT  sqrt(4>3) AS RESULT;
SELECT  sqrt(4.00,0) AS RESULT;
SELECT  sqrt(3++) AS RESULT;




