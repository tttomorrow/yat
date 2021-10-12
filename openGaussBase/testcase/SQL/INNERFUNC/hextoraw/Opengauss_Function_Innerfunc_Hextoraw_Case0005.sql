-- @testpoint: hextoraw函数在查询语句中结合order by使用
--建表
drop table if exists test_tb_hextoraw;
create table test_tb_hextoraw(hex int,hex2 int);
insert into test_tb_hextoraw values(2.58,85);
--查询
select hextoraw(to_char(hex2)),count(hextoraw(to_char(hex2))) from test_tb_hextoraw
group by hextoraw(to_char(hex2)) order by 1,2;
--清理环境
drop table if exists test_tb_hextoraw;