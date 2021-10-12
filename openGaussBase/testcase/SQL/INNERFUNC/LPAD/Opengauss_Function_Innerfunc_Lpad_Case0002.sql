-- @testpoint: lpad函数参数二为空值
SELECT lpad('hi', '','xyza');
SELECT lpad('hi', null,'xyza');