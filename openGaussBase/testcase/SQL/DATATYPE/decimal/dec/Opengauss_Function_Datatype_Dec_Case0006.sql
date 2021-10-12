-- @testpoint: 插入null值

drop table if exists dec_06;
CREATE  TABLE dec_06 (id1 int,id2 DEC(4,2));
insert into dec_06 values (1,null);
insert into dec_06 values (2,'');
select * from dec_06;
drop table dec_06;