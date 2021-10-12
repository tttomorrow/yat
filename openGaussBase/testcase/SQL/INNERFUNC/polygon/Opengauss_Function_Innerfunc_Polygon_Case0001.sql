-- @testpoint: polygon函数将矩形转换成4点多边形
SELECT polygon(box '((0,0),(1,1))') AS RESULT;