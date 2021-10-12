-- @testpoint: 匿名块游标使用 loop循环

drop table if exists t_cur_emp;
create table t_cur_emp(eno int ,en varchar2(200),sal number);
insert into t_cur_emp values(1,'xu',100);
insert into t_cur_emp values(2,'zhang',200);
insert into t_cur_emp values(3,'li',300);

declare
  type cur_type is ref cursor;
  cur    cur_type;
  rec    t_cur_emp%rowtype;
  str    varchar2(200);
  letter char := 'x';
begin
  str := 'select en from t_cur_emp where en like ''%' || letter || '%''';
  open cur for str;
  raise notice 'contain % name：',letter;
  loop
    fetch cur
      into rec.en;
    exit when cur%notfound;
    raise notice '%',rec.en;
  end loop;
  close cur;
end;
/

drop table if exists t_cur_emp;
