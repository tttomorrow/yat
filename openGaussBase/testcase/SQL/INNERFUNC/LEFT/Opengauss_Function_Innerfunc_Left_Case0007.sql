-- @testpoint: left函数入参个数超过固定值，合理报错
select left('xiexiaoyu','gaoxin',5);
select left('xiexiaoyu','gaoxin',4,5);
