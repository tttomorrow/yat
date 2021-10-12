--  @testpoint: --建表查询
DROP TABLE if EXISTS words CASCADE;
CREATE TABLE words(name1 varchar,name2 int);
begin
  for i in 1..20 LOOP
    insert into words VALUES('aa',i);
  end loop;
end;
/
select array_to_json(array_agg(row_to_json(t))) from (select name1, name2 from words) t;

--SELECT row_to_json(words) from words;
DROP TABLE if EXISTS words CASCADE;