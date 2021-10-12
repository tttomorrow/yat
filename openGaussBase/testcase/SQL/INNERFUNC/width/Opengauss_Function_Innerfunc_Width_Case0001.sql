-- @testpoint: 坐标为正坐标，计算矩形水平尺寸

select width(box '((0,0),(1,1))') as result;
