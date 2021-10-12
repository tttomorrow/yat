-- @testpoint: 坐标中有字母，计算矩形水平尺寸,合理报错

select width(box '((1,a),(2,3))') as result;
select width(box '((a,2),(2,3))') as result;