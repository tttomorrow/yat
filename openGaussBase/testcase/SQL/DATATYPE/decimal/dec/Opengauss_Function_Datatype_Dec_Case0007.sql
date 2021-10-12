-- @testpoint: 插入其他无效类型，合理报错

drop table if exists dec_07;
CREATE  TABLE dec_07 (id DEC(4,2));
insert into dec_07 values ('test');
insert into dec_07 values (date'2020-02-02');
insert into dec_07 values (TRUE);
insert into dec_07 values (HEXTORAW('DEADBEEF'));
select * from dec_07;
drop table dec_07;