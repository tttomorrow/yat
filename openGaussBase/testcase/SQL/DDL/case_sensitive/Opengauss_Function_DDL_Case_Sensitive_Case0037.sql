--  @testpoint: 删除视图，区分视图的大小写
drop view VIEW_3;
DROP VIEW view_2;
select * from view_2;
SELECT * FROM VIEW_2 order by 1;
drop view VIEW_2;
DROP VIEW view_3;
SELECT * FROM view_3;
select * from VIEW_2;