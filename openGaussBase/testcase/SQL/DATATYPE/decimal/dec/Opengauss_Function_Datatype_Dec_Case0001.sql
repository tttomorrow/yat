-- @testpoint: 创建行存普通表，精度值在合理范围内，插入数据

drop table if exists dec_01;
create table dec_01 (id dec(4,2)) with (orientation=row, compression=no);
insert into dec_01 values (11.11);
insert into dec_01 values (23.00);
insert into dec_01 values (1.1);
select * from dec_01;
drop table dec_01;