-- @testpoint: polygon函数将圆转换成12点多边形
SELECT polygon(circle '((0,0),2.0)') AS RESULT;