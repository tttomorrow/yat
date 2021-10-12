--  @testpoint:cursor声明游标，使用value子句，子句类型为json类型；


start transaction;
cursor cursor27 for values(array_to_json('{{1,5},{99,100}}'::int[]));
fetch from cursor27;
close cursor27;
end;

