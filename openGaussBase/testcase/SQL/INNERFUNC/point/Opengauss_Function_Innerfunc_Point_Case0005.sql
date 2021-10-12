-- @testpoint: point函数返回多边形的中心
SELECT point(polygon '((0,0),(1,1),(2,0))') AS RESULT;