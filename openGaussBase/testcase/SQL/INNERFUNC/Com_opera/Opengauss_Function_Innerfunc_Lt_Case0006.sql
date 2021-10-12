-- @testpoint: opengauss比较操作符<=，异常校验，合理报错
-- 报错校验，不能隐式转换的不同类型，少参、空值
select point(1,2) <= '22'::smallint as result;
select point(1,2) <= point(3,2) as result;
SELECT (-222::INTEGER,-222::INTEGER) <= 221::INTEGER;
SELECT  <= 221::INTEGER;
SELECT '' <= 221::INTEGER;