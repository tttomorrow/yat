-- @testpoint: polygon函数将圆转换成npts点多边形
SELECT polygon(12, circle '((0,0),2.0)') AS RESULT;