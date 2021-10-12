-- @testpoint: 插入合理范围值

drop table if exists dec_08;
create table dec_08 (id dec(5,2));
insert into dec_08 values (1);
insert into dec_08 values (11);
insert into dec_08 values (1.1);
insert into dec_08 values (0.11);
insert into dec_08 values (111);
insert into dec_08 values (11.1);
insert into dec_08 values (1.11);
insert into dec_08 values (111.1);
insert into dec_08 values (11.11);

select * from dec_08;
drop table dec_08;