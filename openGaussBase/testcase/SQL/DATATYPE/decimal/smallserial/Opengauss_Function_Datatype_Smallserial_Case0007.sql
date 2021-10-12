-- @testpoint: 插入超出右边界范围值，合理报错
-- @modified at: 2020-11-25

begin
  drop table if exists smallserial_07;
  create table smallserial_07 (name smallserial);
  for i in 1 .. 32768 loop
    insert into smallserial_07 values (default);
  end loop;
end;
/
