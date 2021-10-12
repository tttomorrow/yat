--  @testpoint:opengauss关键字password(非保留)，几何函数，几何类型

SELECT isclosed(path '((0,0),(1,1),(2,0))') AS RESULT;

SELECT length(path '((-1,0),(1,0))') AS RESULT;

SELECT npoints(path '[(0,0),(1,1),(2,0)]') AS RESULT;

 SELECT npoints(polygon '((1,1),(0,0))') AS RESULT;

SELECT pclose(path '[(0,0),(1,1),(2,0)]') AS RESULT;

SELECT popen(path '((0,0),(1,1),(2,0))') AS RESULT;

select path'[(1,1),(2,2),(2,1)]';

select path'(1,1),(2,2),(2,1)';

