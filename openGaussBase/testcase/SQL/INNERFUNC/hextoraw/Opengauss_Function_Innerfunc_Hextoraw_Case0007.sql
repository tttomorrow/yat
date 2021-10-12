-- @testpoint: hextoraw函数用于查询语句中结合case when使用
--建表
drop table if exists test_tb_hextoraw;
create table test_tb_hextoraw(hex int,hex1 int);
--插入数据
insert into test_tb_hextoraw values(7788,2585.25),(8899,58);
--查询
select case when hextoraw(hex) !='07788' then hex else hex1 end god from test_tb_hextoraw order by 1;
select hextoraw(case when hex !='7788' then hex else '8899' end) god from test_tb_hextoraw order by 1;
--清理环境
drop table if exists test_tb_hextoraw;