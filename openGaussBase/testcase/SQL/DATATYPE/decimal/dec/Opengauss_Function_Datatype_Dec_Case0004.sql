-- @testpoint: dec数据类型转换至boolean、date，合理报错

drop table if exists dec_04;
CREATE  TABLE dec_04 (id DEC(4,2));
insert into dec_04 values (11.11);
select * from dec_04;

--修改dec数据类型为boolean
alter table dec_04 alter column id type boolean;
--修改dec数据类型为date
alter table dec_04 alter column id type date;
drop table dec_04;