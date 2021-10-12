-- @testpoint: polygon函数将路径转换成多边形
SELECT polygon(path '((0,0),(1,1),(2,0))') AS RESULT;